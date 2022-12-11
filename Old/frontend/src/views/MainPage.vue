<template>
    <main>
        <div class="container container-sm">
            <masonry
                :cols="{default: 6, 1480: 5, 1280: 4, 1080: 3, 780: 2, 500: 1}"
                :gutter="{default: 'var(--margin-main)'}"
                >
                <Filters
                    :minAvailableYear="minYear"
                    :availableMakes="availableMakes"
                    :popularMakes="popularMakes"
                    :availableModels="availableModels"
                    :resultsCount="resultsCount"
                    @changeFilters="changeFilters"
                    />
                <template
                    v-for="car in cars"
                >
                    <AppCarCard
                        :car="car"
                        :key="`car-${car.id}`"
                    />
                </template>
                <infinite-loading
                    v-if="cars.length"
                    @infinite="infiniteHandler"
                    >
                    <div slot="no-results"></div>
                </infinite-loading>
            </masonry>
            <CookiesWarning v-if="userAgreeCookies !== 'true'" />
        </div>
    </main>
</template>

<script>
import qs from 'qs';
import { isCancel } from 'axios';
import InfiniteLoading from 'vue-infinite-loading';
import AppCarCard from '@/components/AppCarCard';
import CookiesWarning from '@/components/CookiesWarning';
import { API } from '@/services/api';
import Filters from '@/components/Filters';

export default {
    name: 'MainPage',
    components: {
        Filters,
        AppCarCard,
        CookiesWarning,
        InfiniteLoading,
    },
    props: {
        page: {
            type: Number,
            default: 1,
        },
    },
    data(props) {
        return {
            cars: [],
            isLoading: false,
            requestsPending: 0,
            maxPage: 1,
            resultsCount: null,
            minYear: 2000,
            availableMakes: [],
            popularMakes: [],
            availableModels: [],
            filtersQueryString: 'only_with_photo=true&is_broken=false',
            perPage: 25,
            currentPage: props.page,
            userAgreeCookies: localStorage.getItem('userAgreeCookies'),
        };
    },
    created() {
        this.isLoading = true;
        this.getMinYear();
        this.getAvailableMakes();
        // We get cars from: getCars() <- changeFilters() <- Filters: @changeFilters="changeFilters" <- watch.filters.emit <- mounted
    },
    methods: {
        getCars(page = 1, filters = '') {
            this.isLoading = true;
            ++this.requestsPending;
            const oldModels = this.availableModels;
            const shouldUpdateModelsList = !this.filtersQueryString.includes('model');
            const isModelReset = this.filtersQueryString.indexOf('isModelReset=true');

            if (isModelReset === -1) {
                this.availableModels = [];
            }

            let filtersQueryString = filters;
            const number = this.filtersQueryString.indexOf('&isModelReset=');
            if (number !== -1) {
                filtersQueryString = filters.substring(0, number);
            } else {
                filtersQueryString = filters;
            }

            API.getCars(page, filtersQueryString)
                .then((res) => {
                    const {
                        count,
                        totalPages,
                        results,
                        makes,
                        models,
                    } = res.data;
                    this.resultsCount = count;
                    this.cars = results;
                    this.maxPage = (totalPages > 99) ? 99 : totalPages;
                    this.popularMakes = makes;
                    this.availableModels = (shouldUpdateModelsList) ? models : oldModels;
                })
                .catch((err) => {
                    if (!isCancel(err)) {
                        console.log(err);
                    }
                })
                .finally(() => {
                    --this.requestsPending;
                    this.isLoading = false;
                });
        },
        getMinYear() {
            API.getMinYear()
                .then((res) => {
                    this.minYear = res.data.min_year;
                })
                .catch((err) => console.log(err));
        },
        getAvailableMakes() {
            API.getMakes()
                .then((res) => {
                    this.availableMakes = res.data;
                    this.popularMakes = res.data;
                })
                .catch((err) => console.log(err));
        },
        pageClicked(newPage) {
            API.cancelRequest();
            // redirect if we are not on that page already
            if (parseInt(this.$route.query.page || '1', 10) !== newPage) {
                this.$router.push({
                    name: 'Main Page',
                    query: { page: newPage },
                });
                return;
            }

            this.getCars(newPage, this.filtersQueryString);
        },
        changeFilters(filters) {
            this.perPage = parseInt(filters.items_per_page, 10) || 50;
            console.log('filters', filters);
            console.log('this.filtersQueryString', this.filtersQueryString);
            this.filtersQueryString = qs.stringify(filters, { indices: false });
            this.pageClicked(1);
        },
        infiniteHandler($state) {
            API.getCars(this.currentPage + 1, this.filtersQueryString)
                .then((res) => {
                    this.cars.push(...res.data.results);
                    $state.loaded();
                })
                .catch((err) => {
                    console.log(err);
                    $state.complete();
                });
            if (this.currentPage + 1 === this.maxPage) {
                $state.complete();
            }
            ++this.currentPage;
        },
    },
    watch: {
        // eslint-disable-next-line func-names
        '$route.query': (val) => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth',
            });

            // Firefox bug: without setTimeout scrollTo doesn't happen
            setTimeout(() => this.getCars(val.page, this.filtersQueryString), 100);
        },
    },
};
</script>

<style lang="scss" scoped>

main {
    width: 100%;
    height: fit-content;
    display: flex;
    flex: 1 0 auto;
    padding-right: var(--margin-main);
}

section {
    // max-width: 920px;
    // margin-right: 20px;
    width: 100%;
    // padding: 40px 0;
    box-sizing: content-box;
    display: flex;
}

aside {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin: 40px 0;
    padding-bottom: 40px;
}

.pagination-container {
    padding: 16px;
    display: flex;
    justify-content: center;
}

.no-results {
    padding: 0 16px;
    font-size: 24px;
    max-width: 920px;
    margin: 32px auto;
    text-align: center;
}

.no-more-records {
    font-size: 18px;
    color: grey;
    margin: 20px auto;
    text-align: center;
}

.cars-list {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-gap: 1rem;
}

@media screen and (max-width: 1300px) {
    section {
        margin-right: 0;
    }

    aside {
        display: none;
    }
}

@media screen and (max-width: 1000px) {
    .pagination-container {
        margin-right: 5%;
    }
}

</style>
