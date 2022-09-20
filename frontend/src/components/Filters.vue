<template>
    <div class="filters-container">
        <table  class="filters" ref="filtersBlock">
            <tbody>
                <tr class="filters__filter--location">
                    <td>Location:</td>
                    <td>
                        <BaseLocation
                            :userCity="filters.location"
                            :distance="filters.distance"
                            @changeLocation="changeUserLocation"
                            @changeLocationOffset="changeDistance"
                        />
                    </td>
                </tr>
                <tr class="filters__filter--make">
                    <td>Make:</td>
                    <td>
                        <BaseSelect
                            placeholder="Any"
                            :strictFilter="true"
                            :options="availableMakes.map((item) => item.make).sort()"
                            :selectedOption="filters.make"
                            @selectOption="(option) => {filters.model = ''; filters.make = option;}"
                            @resetSelectedOptions="filters.make = ''; isModelReset = false;"
                            withInput
                        />
                    </td>
                </tr>
                <tr class="filters__filter--model">
                    <td>Model:</td>
                    <td>
                        <BaseSelect
                            class="filters__item_large"
                            :placeholder="'–'"
                            :strictFilter="true"
                            :options="modelsList"
                            :selectedOption="filters.model"
                            @selectOption="(option) => {this.isModelReset = false;return filters.model = option;   } "
                            @resetSelectedOptions="onResetSelectedOptions()"
                            :disabled="!this.modelsList.length"
                            withInput
                        />
                    </td>
                </tr>
                <tr class="filters__filter--year">
                    <td>Year:</td>
                    <td class="filters__group">
                        <BaseSelect
                            placeholder="1886"
                            :options="yearFromOptions"
                            :selectedOption="filters.year_from"
                            @selectOption="(option) => filters.year_from = option"
                            @resetSelectedOptions="filters.year_from = ''; isModelReset = false;"
                            resetText="Reset"
                            bordersType="left"
                            withInput
                            onlyNumbers
                        />
                        <span>–</span>
                        <BaseSelect
                            :placeholder="new Date().getFullYear() + ''"
                            :options="yearToOptions"
                            :selectedOption="filters.year_to"
                            @selectOption="(option) => filters.year_to = option"
                            @resetSelectedOptions="filters.year_to = ''; isModelReset = false;"
                            resetText="Reset"
                            bordersType="right"
                            withInput
                            onlyNumbers
                        />
                    </td>
                </tr>
                <tr class="filters__filter--mileage">
                    <td>Mileage:</td>
                    <td class="filters__group">
                        <BaseInput
                            class="filters__item_grouped"
                            placeholder="0"
                            v-model="filters.mileage_from"
                            bordersType="left"
                            showUnits="mi"
                        />
                        <span>–</span>
                        <BaseInput
                            class="filters__item_grouped"
                            placeholder="∞"
                            v-model="filters.mileage_to"
                            bordersType="right"
                            showUnits="mi"
                            :from-value="filters.mileage_from"
                        />
                    </td>
                </tr>
                <tr class="filters__filter--price">
                    <td>Price:</td>
                    <td class="filters__group">
                        <BaseInput
                            class="filters__item_grouped"
                            placeholder="0"
                            v-model="filters.price_from"
                            bordersType="left"
                            showUnits="$"
                        />
                        <span>–</span>
                        <BaseInput
                            class="filters__item_grouped"
                            placeholder="∞"
                            v-model="filters.price_to"
                            bordersType="right"
                            showUnits="$"
                            :fromValue="filters.price_from"
                        />
                    </td>
                </tr>
                <tr class="filters__filter--color">
                    <td>Color:</td>
                    <td>
                        <BaseColor @changeColors="changeColors"/>
                    </td>
                </tr>
                <tr class="filters__filter--is-new">
                    <td>New/Used:</td>
                    <td>
                        <BaseRadioButtonGroup
                            :options="['All', 'New', 'Used']"
                            :selectedOption="isNewSelectedOption"
                            @selectOption="selectIsNew"
                        />
                    </td>
                </tr>
                <tr class="filters__filter--condition">
                    <td>Condition:</td>
                    <td>
                        <BaseRadioButtonGroup
                            :options="['All', 'Working', 'Broken']"
                            :selectedOption="(filters.is_new) ? null : isBrokenSelectedOption"
                            :disabled="!!filters.is_new"
                            @selectOption="selectIsBroken"
                        />
                    </td>
                </tr>
                <tr class="filters__filter--body">
                    <td>Body Style:</td>
                    <td>
                        <BaseSelect
                            class="filters__item_small"
                            placeholder="Body"
                            :options="bodyOptions"
                            :selectedOption="filters.body"
                            @selectOption="(option) => filters.body = option"
                            @resetSelectedOptions="filters.body = ''; isModelReset = false;"
                        />
                    </td>
                </tr>
                <tr class="filters__filter--transmission">
                    <td>Transmission:</td>
                    <td>
                        <BaseSelect
                            class="filters__item_small"
                            placeholder="Transmission"
                            :options="transmissionOptions"
                            :selectedOption="filters.transmission"
                            @selectOption="(option) => filters.transmission = option"
                            @resetSelectedOptions="filters.transmission = ''; isModelReset = false;"
                        />
                    </td>
                </tr>
                <tr class="filters__filter--drivetrain">
                    <td>Drivetrain:</td>
                    <td>
                        <BaseSelect
                            class="filters__item_small"
                            placeholder="Drivetrain"
                            :options="driveOptions"
                            :selectedOption="filters.drive"
                            @selectOption="(option) => filters.drive = option"
                            @resetSelectedOptions="filters.drive = ''; isModelReset = false;"
                        />
                    </td>
                </tr>
                <tr class="filters__filter--only-with-photo">
                    <td>Photo Required:</td>
                    <td>
                        <BaseCheckbox
                            class="filters__item_small filters__item_align-right filters__checkbox"
                            label="With photos"
                            v-model="filters.only_with_photo"
                        />
                    </td>
                </tr>
                <tr class="filters__filter--power">
                    <td>Power:</td>
                    <td class="filters__group">
                        <BaseInput
                            class="filters__item_grouped"
                            placeholder="Power from, hp"
                            v-model="filters.power_from"
                            bordersType="left"
                            showUnits="hp"
                        />
                        <span>–</span>
                        <BaseInput
                            class="filters__item_grouped"
                            placeholder="to"
                            v-model="filters.power_to"
                            bordersType="right"
                            showUnits="hp"
                            :from-value="filters.power_from"
                        />
                    </td>
                </tr>
                <tr class="filters__filter--order">
                    <td>Order by:</td>
                    <td>
                        <BaseSelect
                            class="filters__item_small filters__per-page"
                            placeholder="Distance"
                            :options="sortByOptions"
                            :selectedOption="filters.ordering"
                            @selectOption="(option) => filters.ordering = option"
                            hideResetOption
                            valuePrependText=""
                        />
                    </td>
                </tr>
                <tr>
                    <td></td>
                    <td>
                        <div class="filters__reset-filters" v-if="appliedFiltersCount" @click="resetFilters">
                            Reset filters
                            <font-awesome-icon class="filters__reset-filters-icon" :icon="['fas', 'times']"/>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>

        <div class="filters__available-models" v-if="modelsList.length && filters.make && !filters.model">
            <div class="filters__models-items">
                <div
                    class="filters__models-item"
                    v-for="model in availableModels.slice(0, 12)"
                    :key="model.model"
                >
                    <div class="filters__models-item-name" @click="filters.model = model.model">
                        {{ model.model }}
                    </div>
                    <div class="filters__models-item-count">
                        {{ model.count }}
                    </div>
                </div>
            </div>
        </div>

        <div class="filters__available-models" v-if="makesList.length && !filters.make ">
            <div class="filters__models-items">
                <div
                    class="filters__models-item"
                    v-for="make in mostPopularMakes"
                    :key="make.make"
                >
                    <div class="filters__models-item-name" @click="filters.make = make.make">
                        {{ make.make }}
                    </div>
                    <div class="filters__models-item-count">
                        {{ make.count }}
                    </div>
                </div>
            </div>
        </div>

        <div class="filters__hint-top" v-if="showHintTop">
            <div class="filters__hint-title" @click="scrollToTop">
                <svg class="filters__hint-arrow-icon" viewBox="0 0 24 24" id="arrow-rounded">
                    <path fill-rule="evenodd" fill="currentColor"
                          d="M15.483 9.297l-3.9 3.9-3.9-3.9a.99.99 0 00-1.4
                    1.4l4.593 4.593a1 1 0 001.414 0l4.593-4.593a.99.99 0 10-1.4-1.4z"></path>
                </svg>
                {{ appliedFiltersMessage }}
            </div>
            <div class="filters__hint-results-count" v-if="resultsCount">
                {{ resultsCountFormatted }} results
            </div>
        </div>
    </div>
</template>

<script>
import BaseSelect from '@/components/Base/BaseSelect';
import BaseCheckbox from '@/components/Base/BaseCheckbox';
import BaseInput from '@/components/Base/BaseInput';
import BaseLocation from '@/components/Base/BaseLocation';
import BaseRadioButtonGroup from '@/components/Base/BaseRadioButtonGroup';
import BaseColor from '@/components/Base/BaseColor';
import eventBus from '@/eventBus';
import { API } from '@/services/api';
import { getStatesCities } from '@/utils/cities';

const DEFAULT_FILTERS = {
    is_new: null,
    is_broken: false,
    make: '',
    model: '',
    drive: '',
    transmission: '',
    body: '',
    only_with_photo: true,
    year_from: '',
    year_to: '',
    mileage_from: '',
    mileage_to: '',
    price_from: '',
    price_to: '',
    power_from: '',
    power_to: '',
    longitude: 0,
    latitude: 0,
    ordering: 'Distance',
    items_per_page: '25 per page',
    location: '',
    distance: 'Any',
    color: [],
};
export default {
    name: 'Filters',
    components: {
        BaseLocation,
        BaseInput,
        BaseCheckbox,
        BaseSelect,
        BaseRadioButtonGroup,
        BaseColor,
    },
    props: {
        minAvailableYear: {
            type: Number,
            default: 1886,
        },
        availableMakes: {
            type: Array,
            default: () => [],
        },
        popularMakes: {
            type: Array,
            default: () => [],
        },
        availableModels: {
            type: Array,
            default: () => [],
        },
        resultsCount: {
            type: Number,
            default: 0,
        },
    },
    data() {
        // snake case is used to provide valid querystring for backend
        return {
            isModelReset: false,
            filters: { ...DEFAULT_FILTERS },
            driveOptions: [
                'AWD',
                'RWD',
                'FWD',
            ],
            transmissionOptions: [
                'Automatic',
                'Manual',
            ],
            bodyOptions: [
                'Hatchback',
                'Coupe',
                'Convertible',
                'Sedan',
                'SUV',
                'Pickup Truck',
                'Commercial',
                'Minivan',
                'Wagon',
            ],
            sortByOptions: [
                'Distance',
                'Price, lowest first',
                'Price, highest first',
                'Year, lowest first',
                'Year, highest first',
            ],
            itemsPerPageOptions: [
                '25 per page',
                '50 per page',
                '100 per page',
            ],
            showHintTop: false,
        };
    },
    computed: {
        resultsCountFormatted() {
            return new Intl.NumberFormat('en-US').format(this.resultsCount);
        },
        yearsRange() {
            // an array of [min_available_year; current_year]
            const yearsRange = new Date().getFullYear() - this.minAvailableYear + 1;
            return Array.from(new Array(yearsRange), (x, i) => (i + this.minAvailableYear).toString()).reverse();
        },
        yearFromOptions() {
            if (!this.filters.year_to) {
                return this.yearsRange;
            }
            return this.yearsRange.filter((year) => parseInt(year, 10) <= this.filters.year_to);
        },
        yearToOptions() {
            if (!this.filters.year_from) {
                return this.yearsRange;
            }
            return this.yearsRange.filter((year) => parseInt(year, 10) >= this.filters.year_from);
        },
        makesList() {
            let makes = this.popularMakes.map((item) => item.model);
            makes = makes.filter((item) => ((item) ? item.length > 0 : false));
            return makes;
        },
        modelsList() {
            let models = this.availableModels.map((item) => item.model);
            models = models.filter((item) => ((item) ? item.length > 0 : false));
            models.sort();
            return models;
        },
        isNewSelectedOption() {
            return {
                null: 'All',
                true: 'New',
                false: 'Used',
            }[this.filters.is_new];
        },
        isBrokenSelectedOption() {
            return {
                null: 'All',
                true: 'Broken',
                false: 'Working',
            }[this.filters.is_broken];
        },
        appliedFilters() {
            // select not empty values from filters object
            const reduce = Object.keys(this.filters)
                .reduce((acc, key) => {
                    const value = this.filters[key];
                    // Either a boolean or a 'truthy' value
                    // Also we make an exception for distance because we do want to pass '&distance=0'
                    if (typeof value === 'boolean' || value || (key === 'distance' && value !== '')) {
                        acc[key] = value;
                    }
                    return acc;
                }, {});
            reduce.isModelReset = this.isModelReset;
            return reduce;
        },
        appliedFiltersInfo() {
            const appliedFiltersInfo = [];
            let appliedFiltersCount = 0;
            // That is, if we display all cars to the user
            if (!('is_broken' in this.appliedFilters)) appliedFiltersCount += 1;
            Object.entries(this.appliedFilters)
                .forEach(([key, value]) => {
                    switch (key) {
                    case 'make':
                    case 'model':
                        appliedFiltersInfo.push(value);
                        break;
                    case 'location':
                    case 'distance':
                    case 'longitude':
                    case 'latitude':
                    case 'ordering':
                    case 'items_per_page':
                        break;
                    default:
                        if (key === 'is_broken' && value === false) break;
                        if (key === 'only_with_photo' && value === true) break;
                        // if (key === 'ordering' && value === 'distance') break;
                        // if (key === 'items_per_page' && value === '25 per page') break;
                        appliedFiltersCount += 1;
                        break;
                    }
                });
            return [appliedFiltersInfo, appliedFiltersCount];
        },
        appliedFiltersMessage() {
            const [appliedFiltersInfo, appliedFiltersCount] = this.appliedFiltersInfo;
            let result = (appliedFiltersInfo.length) ? appliedFiltersInfo.join(' ') : 'Any model';
            result += (appliedFiltersCount) ? `, ${appliedFiltersCount} parameters` : '';
            return result;
        },
        appliedFiltersCount() {
            return this.appliedFiltersInfo[1];
        },
        mostPopularMakes() {
            const tempMakes = this.popularMakes;
            for (let i = 0; i < tempMakes.length; i++) {
                if (tempMakes[i].make === 'Unknown') {
                    tempMakes.splice(i, 1);
                }
            }
            return tempMakes.sort((first, second) => second.count - first.count).slice(1, 17);
        },
    },
    created() {
        window.addEventListener('scroll', this.onScroll);
    },
    async mounted() {
        eventBus.$on('reset-filters', this.resetFilters);
        const userCity = await this.getUserCity();
        const allOptions = getStatesCities();
        const optionOfUserCity = allOptions.filter((option) => option.name.toLowerCase()
            .startsWith(userCity.city.toLowerCase()))[0];
        if (optionOfUserCity) {
            this.filters.location = `${optionOfUserCity.name}, ${optionOfUserCity.stateCode}`;
            this.filters.longitude = optionOfUserCity.longitude;
            this.filters.latitude = optionOfUserCity.latitude;
        } else {
            this.filters.location = `${userCity.city}`;
            this.filters.longitude = `${Number(userCity.longitude).toFixed(8)}`;
            this.filters.latitude = `${Number(userCity.latitude).toFixed(8)}`;
        }
    },
    destroyed() {
        window.removeEventListener('scroll', this.onScroll);
        eventBus.$off('reset-filters');
    },
    methods: {
        async getUserCity() {
            return API.getUserCity()
                .then((res) => res.data)
                .catch((err) => {
                    console.log(err);
                });
        },
        scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth',
            });
        },
        onResetSelectedOptions() {
            this.filters.model = '';
            this.isModelReset = true;
        },
        onScroll() {
            const { filtersBlock } = this.$refs;
            const rect = filtersBlock.getBoundingClientRect();
            const isVisible = rect.bottom > 0;
            this.showHintTop = !isVisible;
        },
        changeUserLocation(location, distance) {
            this.filters.location = location.name;
            if (location.stateCode) {
                this.filters.location += `, ${location.stateCode}`;
            }
            this.filters.distance = distance;
            this.filters.longitude = location.longitude;
            this.filters.latitude = location.latitude;
        },
        changeDistance(distance) {
            this.filters.distance = distance;
        },
        changeColors(colors) {
            this.filters.color = colors;
        },
        resetFilters() {
            this.filters = { ...DEFAULT_FILTERS };
            eventBus.$emit('clear-form');
        },
        sortByForQuery(param) {
            return {
                Distance: 'distance',
                'Price, lowest first': 'price',
                'Price, highest first': '-price',
                'Year, lowest first': 'year',
                'Year, highest first': '-year',
            }[param];
        },
        selectIsNew(option) {
            switch (option) {
            case 'New':
                this.filters.is_new = true;
                // new car can't be broken, resetting is_broken filter
                this.filters.is_broken = false;
                break;
            case 'Used':
                this.filters.is_new = false;
                break;
            default:
                this.filters.is_new = null;
                break;
            }
        },
        selectIsBroken(option) {
            switch (option) {
            case 'Working':
                this.filters.is_broken = false;
                break;
            case 'Broken':
                this.filters.is_broken = true;
                break;
            default:
                this.filters.is_broken = null;
                break;
            }
        },
    },
    watch: {
        filters: {
            handler() {
                const { ordering } = this.appliedFilters;
                const normalizedOrdering = this.sortByForQuery(ordering);
                if (normalizedOrdering) {
                    this.appliedFilters.ordering = normalizedOrdering;
                } else {
                    delete this.appliedFilters.ordering;
                }
                this.$emit('changeFilters', this.appliedFilters);
            },
            deep: true,
        },
    },
};
</script>

<style lang="scss" scoped>
@import '@/_vars.scss';

.filters {
    margin-bottom: 24px;
    /* padding: 20px; */
    // border-radius: 8px;
    /* background: #FFF; */
    /* box-shadow: 0 3px 14px rgb(0 0 0 / 12%); */
    position: -webkit-sticky;
    position: sticky;
    top: var(--margin-main);
    // display: flex;
    // flex-direction: column;
    // justify-content: space-between;
    max-height: calc(100vh - 2 * var(--margin-main));
    // width: 100%;
    border: 2px solid black;
    // box-shadow: 5px 5px 0 black;
    border: 2px solid black;
    padding: 0 10px 10px 10px;

    tr td {
        vertical-align: bottom;
        align-self: flex-end;
        // font-family: monospace;
        padding-top: 10px;
    }

    tr td:first-child {
        // max-width: calc(var(--filters-width) * 0.4);
        text-transform: capitalize;
        // font-size: 1.2rem;
        padding-right: calc(var(--margin-main) / 4);
        text-align: end;
        font-weight: bold;
        text-transform: uppercase;
        white-space: nowrap;
    }

    tr td:last-child {
        // width: 100%;
        border-bottom: 1px solid var(--color--black);
        // width: calc(var(--filters-width) * 0.6);
    }

    tr:last-child td:last-child {
        border-bottom: none;
    }

    &__group {
        display: flex;
        justify-content: space-between;
    }

    &__filter--color,
    &__filter--mileage,
    &__filter--is-new,
    &__filter--condition,
    &__filter--body,
    &__filter--transmission,
    &__filter--drivetrain,
    &__filter--only-with-photo,
    &__filter--power {
        display: none;
    }

    &__row {
        display: flex;
        // margin: 5px 0;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 10px;

        &_header {
            margin-top: 0;
        }
        &_last {
            margin-bottom: 0;
        }
        &_colors-phone {
            display: none;
        }
    }

    &__column {
        width: 33.34%;
        display: flex;
        align-items: center;
        margin-left: 20px;
        &:first-child {
            margin-left: 0;
        }
        &_align-right {
            justify-content: flex-end;
        }
        &-top {
            z-index: 100;
        }
    }
    &__item {
        &_large {
            // width: 100%;
        }
        &_small {
            // width: calc(50% - 5px);
            &:first-of-type {
                // margin-right: 10px;
            }
        }
        &_grouped {
            // width: 50%;
        }
        &_align-right {
            justify-content: flex-end;
        }
    }
    &__reset-filters {
        color: grey;
        font-size: 15px;
        line-height: 24px;
        display: flex;
        margin: auto;
        justify-content: center;
        align-items: center;
        transition: color .3s ease;
        flex-shrink: 0;
        &:hover {
            color: $accent-color;
            cursor: pointer;
        }
    }
    &__reset-filters-icon {
        margin-left: 8px;
    }
    &__results-count {
        font-size: 15px;
        color: grey;
        margin: 10px 35px 0 auto;
        width: 100%;
        text-align: right;
    }
    &__hint-top {
        top: 0;
        font-size: 15px;
        position: fixed;
        z-index: 3000;
        display: flex;
        justify-content: space-between;
        align-items: center;
        overflow: hidden;
        width: 920px;
        height: 44px;
        // border-radius: 0 0 8px 8px;
        background: #fff;
        box-shadow: 0 3px 14px rgb(0 0 0 / 12%);
        transition: top .2s;
    }
    &__hint-title {
        line-height: 44px;
        transition: color .3s ease;
        &:hover {
            cursor: pointer;
            color: $accent-color;
        }
    }
    &__hint-arrow-icon {
        width: 24px;
        height: 24px;
        margin: 0 8px 0 16px;
        vertical-align: middle;
        transform: rotate(180deg) translateY(2px);
    }
    &__hint-results-count {
        line-height: 44px;
        margin: 0 24px 0 auto;
        color: grey;
    }
    &__below-selects {
        width: 100%;
        display: flex;
        margin: 0 auto 16px 16px;
    }
    &__available-models {
        padding: 24px 16px 9px;
        margin-bottom: 15px;
    }
    &__models-items {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
    }
    &__models-item {
        font-size: 15px;
        line-height: 18px;
        position: relative;
        display: flex;
        justify-content: space-between;
        width: 210px;
        margin: 0 12px 15px 0;
        white-space: nowrap;
    }
    &__models-item-name {
        position: relative;
        z-index: 2;
        overflow: hidden;
        flex-shrink: 0;
        max-width: 84%;
        padding-right: 8px;
        text-overflow: ellipsis;
        font-size: 15px;
        color: #157ee1;
        &:hover {
            cursor: pointer;
            color: $accent-color;
        }
    }
    &__models-item-count {
        position: relative;
        z-index: 2;
        display: flex;
        width: 100%;
        margin-left: auto;
        color: grey;
        &::before {
            width: 100%;
            margin-right: 8px;
            margin-bottom: 4px;
            content: "";
            border-bottom: 1px solid #e0e0e0;
        }
    }
    &__per-page {
        max-width: 174px;
    }
    &__sort-by {
        min-width: 245px;
        max-width: 350px;
    }
    tr td:second-child {
        color: green;
    }
}
@media screen and (max-width: 1000px) {
    .filters {
        width: auto;
        &__row {
            width: 100%;
            gap: 10px;
            &_header {
                flex-direction: column;
                gap: 16px;
                flex-direction: column-reverse;
            }
            &:nth-of-type(3), &:nth-of-type(4) {
                flex-direction: column;
                gap: 16px;
            }
        }
        &__column {
            width: 100%;
            margin: 0;
        }
        &__checkbox {
            justify-content: flex-start;
        }
        &__hint-top {
            width: calc(100% - 10%);
        }
        &__below-selects {
            width: auto;
            margin-bottom: 16px;
            justify-content: end;
        }
        &__available-models {
            margin: 0;
            padding: 0;
        }
        &__models-items {
            grid-template-columns: repeat(2, 1fr);
        }
        &__models-item {
            width: auto;
        }
        &__results-count {
            margin: 10px 2px 0 auto;
        }
    }
}

@media screen and (max-width: 920px) {
    .filters {
        &__row_colors-phone {
            display: flex;
        }
        &__column_colors-laptop {
            display: none;
        }
    }
}

@media screen and (max-width: 660px) {
    .filters {
        &__column {
            margin-bottom: 20px;
        }
        &__row {
            display: initial;
            &_header {
                display: flex;
                .filters {
                    &__column {
                        margin-bottom: 10px;
                    }
                }
            }
        }
    }
}

@media screen and (max-width: 360px) {
    .filters {
        padding: 20px 11px;
        &__hint-top {
            flex-direction: column;
            align-items: flex-start;
            height: auto;
        }
        &__hint-results-count {
            margin: 0;
            margin-left: 20px;
        }
    }
}

</style>
