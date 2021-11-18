<template>
    <main>
        <div class="container container-sm">
            <section>
                <Filters
                    :minAvailableYear="minYear"
                    :availableMakes="availableMakes"
                    :availableModels="availableModels"
                    :resultsCount="resultsCount"
                    @changeFilters="changeFilters"
                />
                <div v-if="isLoading || requestsPending > 0">
                    <component
                        v-for="_ in perPage"
                        :key="_"
                        :is="($store.getters.showMobile) ? 'ContentPlaceholderCardMobile' : 'ContentPlaceholderCard'"
                    />
                </div>
                <div v-else-if="resultsCount !== 0">
                    <AppCarsList
                        class="cars-list"
                        :cars="cars"
                    />
                    <infinite-loading
                        v-if="$store.getters.showMobile && cars.length"
                        @infinite="infiniteHandler"
                    >
                        <div slot="no-results" class="no-more-records">No more records</div>
                    </infinite-loading>

                    <div class="pagination-container" v-else>
                        <paginate
                            :value="page"
                            :pageCount="maxPage"
                            :clickHandler="pageClicked"
                            :pageRange="7"
                            :prevText="'←'"
                            :nextText="'→'"
                            :containerClass="'pagination'"
                            :pageClass="'page-item'"
                            :pageLinkClass="'page-item-link'"
                            :activeClass="'page-item-active'"
                            :disabledClass="'page-item-disabled'"
                            :prevClass="'page-item-prev'"
                            :nextClass="'page-item-next'"
                            :prevLinkClass="'page-item-link'"
                            :nextLinkClass="'page-item-link'"
                        />
                    </div>
                </div>
                <p v-else class="no-results">
                    Unfortunately we could not find any cars for you. Please try to change the filters.
                </p>
            </section>

            <aside>
                <AdLargeSkyscraper />
            </aside>
            <CookiesWarning v-if="userAgreeCookies !== 'true'" />
        </div>
    </main>
</template>

<script>
import qs from 'qs';
import { isCancel } from 'axios';
import InfiniteLoading from 'vue-infinite-loading';
import AppCarsList from '@/components/AppCarsList';
import ContentPlaceholderCard from '@/components/ContentPlaceholderCard';
import ContentPlaceholderCardMobile from '@/components/ContentPlaceholderCardMobile';
import CookiesWarning from '@/components/CookiesWarning';
import { API } from '@/services/api';
import Filters from '@/components/Filters';
import AdLargeSkyscraper from '@/components/Ads/AdLargeSkyscraper';

export default {
    name: 'MainPage',
    components: {
        Filters,
        AppCarsList,
        ContentPlaceholderCard,
        ContentPlaceholderCardMobile,
        AdLargeSkyscraper,
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
                        models,
                    } = res.data;
                    this.resultsCount = count;
                    this.cars = results;
                    this.maxPage = (totalPages > 99) ? 99 : totalPages;
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
                    this.availableMakes = res.data.map((item) => item.make);
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
        '$route.query': function (val) {
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
}

section {
    margin-right: 20px;
    width: 100%;
    padding: 40px 0;
    box-sizing: content-box;
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
