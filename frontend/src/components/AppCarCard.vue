<template>
    <div class="root" v-if="$store.getters.showMobile">
        <div class="card-m">
            <a :href="car.url" class="card__link" target="_blank" rel="noreferrer">
                <div class="card-m__header">
                    <p class="card-m__title">
                        {{ title }}<span v-if="car !== 0">, {{ car.year }}</span><span v-else>-</span>
                    </p>
                    <h3 class="card-m__price">
                        {{ price }}
                    </h3>
                </div>

                <div class="card-m__gallery" v-if="photosLoaded">
                    <img
                        class="card-m__photo"
                        v-for="(photo, index) in previewPhotos"
                        :key="index"
                        :src="getPhoto(index)"
                    />
                </div>
                <div v-else class="card-m__gallery">
                    <content-placeholders :rounded="true">
                        <content-placeholders-img class="card-m__photo" />
                        <content-placeholders-img class="card-m__photo" />
                        <content-placeholders-img class="card-m__photo" />
                    </content-placeholders>
                </div>

                <div class="card-m__params">
                    <div class="card-m__params-column">
                        <div class="card-m__params-cell">{{ power }}</div>
                        <div class="card-m__params-cell">{{ transmission }}</div>
                        <div class="card-m__params-cell">{{ mileage }}</div>
                    </div>
                    <div class="card-m__params-column">
                        <div class="card-m__params-cell">{{ drive }}</div>
                        <div class="card-m__params-cell">{{ body }}</div>
                    </div>
                </div>
                <div class="card-m__footer">
                    <div class="card-m__location">
                        {{ car.location }}
                    </div>
                    <div class="card-m__source">
                        {{ car.source }}
                    </div>
                </div>
            </a>
        </div>
    </div>
    <div class="card" v-else>
        <div class="card__main">
            <a :href="car.url" class="card__link" target="_blank" rel="noreferrer">
                <div class="card__thumb">
                    <GalleryOnHover
                        v-if="photosLoaded"
                        :photos="previewPhotos"
                        :totalPhotos="totalPhotos"
                        :placeholder-url="placeholderPhotoUrl"
                    />
                    <content-placeholders v-else :rounded="true">
                        <content-placeholders-img class="card__img" />
                    </content-placeholders>
                </div>
                <div class="card__clicker"></div>
            </a>
            <div class="card__description">
                <div class="card__column">
                    <div class="card__column-row">
                        <h3 class="card__title">{{ title }}</h3>
                    </div>
                    <div class="card__column-row">
                        <div class="card__tech-summary">
                            <div class="card__tech-summary-column">
                                <div class="card__cell" title="Power">{{ power ? `${power} hp` : power }}</div>
                                <div class="card__cell" title="Transmission">{{ transmission }}</div>
                            </div>
                            <div class="card__tech-summary-column">
                                <div class="card__cell" title="Drivetrain">{{ drive }}</div>
                                <div class="card__cell" title="Body Style">{{ body }}</div>
                            </div>
                        </div>
                    </div>

                    <div class="card__column-row">
                        <div v-if="present(car.location)" class="card__additional-info">
                            {{ car.location }}
                        </div>
                    </div>
                </div>

                <div class="card__column">
                    <div class="card__column-row">
                        <div class="card__price">{{ price }}</div>
                    </div>
                </div>

                <div class="card__column">
                    <div class="card__column-row">
                        <div class="card__year">{{ year }}</div>
                    </div>
                </div>

                <div class="card__column">
                    <div class="card__column-row">
                        <div v-if="present(car.mileage)" class="card__mileage">
                            {{ mileage }}
                        </div>
                    </div>

                    <div class="card__column-row">
                        <div
                            v-if="present(car.source)"
                            class="card__additional-info card__additional-info_align_right"
                        >
                            {{ car.source }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import GalleryOnHover from '@/components/GalleryOnHover';

export default {
    name: 'AppCarCard',
    components: { GalleryOnHover },
    props: {
        car: {
            required: true,
            type: Object,
        },
    },
    data() {
        return {
            photosLoaded: false,
        };
    },
    created() {
        this.preloadPhotos();
    },
    computed: {
        title() {
            if (this.car.make && this.car.model) {
                return `${this.car.make} ${this.car.model}`;
            }
            return this.car.title;
        },
        price() {
            if (!this.car.price) {
                return 'No price';
            }
            const USFormat = Intl.NumberFormat('en-US');
            return `$${USFormat.format(this.car.price)}`;
        },
        year() {
            if (this.car.year !== 0) {
                return this.car.year;
            }
            return '';
        },
        mileage() {
            if (!this.car.mileage) {
                const currentYear = new Date().getFullYear();
                if (this.car.year === currentYear || this.car.year === currentYear + 1) {
                    return 'New';
                }
                return '';
            }
            const USFormat = Intl.NumberFormat('en-US');
            return `${USFormat.format(this.car.mileage)} mi`;
        },
        power() {
            if (!this.car.power) return '';
            return this.car.power;
        },
        transmission() {
            if (this.car.transmission === 'Unknown') return '';
            return this.car.transmission;
        },
        drive() {
            if (this.car.drive === 'Unknown') return '';
            return this.car.drive;
        },
        body() {
            if (this.car.body === 'Unknown') return '';
            return this.car.body;
        },
        previewPhotos() {
            if (this.car.photos) return this.car.photos.slice(0, 5);
            return [];
        },
        totalPhotos() {
            if (this.car.photos) return this.car.photos.length;
            return 0;
        },
        placeholderPhotoUrl() {
            return `https://via.placeholder.com/200x150?text=${this.title}`;
        },
    },
    methods: {
        present(property) {
            return property !== 'nan' && property !== '';
        },
        preloadPhotos() {
            this.photosLoaded = false;

            if (!this.previewPhotos.length) {
                this.photosLoaded = true;
                return;
            }

            let loadedCount = 0;
            this.previewPhotos.map((photo) => {
                const img = new Image();
                img.onload = () => {
                    ++loadedCount;
                    if (loadedCount === this.previewPhotos.length) {
                        this.photosLoaded = true;
                    }
                };
                img.onerror = () => {
                    img.src = this.placeholderPhotoUrl;
                };
                img.src = photo;
                return img;
            });
        },
        getPhoto(index) {
            if (!this.previewPhotos || this.previewPhotos[0] === '') {
                return this.placeholderPhotoUrl;
            }
            return this.previewPhotos[index];
        },
        navigateToSource() {
            window.open(this.car.url, '_blank');
        },
    },
};
</script>

<style lang="scss" scoped>
@import '@/_vars';

.root {
    width: 100%;
}

.card {
    width: 100%;
    position: relative;
    padding: 16px;
    background-color: $white;
    z-index: 1;

    &:hover {
        z-index: 2;
        border-radius: 8px;
        background-color: #fff;
        box-shadow: 0 5px 20px 0 $card-shadow-color;
    }

    &::before {
        position: absolute;
        top: 0;
        right: 16px;
        left: 16px;
        display: block;
        height: 1px;
        content: " ";
        border-top: 1px solid $divider-color;
    }

    &:hover:before {
        display: none;
    }

    &:hover + .card::before {
        display: none;
    }

    &:hover .card__title {
        color: $accent-color;
    }

    &__main {
        display: flex;
    }

    &__thumb {
        flex-shrink: 0;
        width: 205px;
        height: 150px;
    }

    &__img {
        width: 205px;
        height: 150px;
        border-radius: 8px;
    }

    &__description {
        display: flex;
        padding: 0 16px;
        justify-content: space-between;
        width: 100%;
    }

    &__title {
        font-size: 17px;
        font-weight: 700;
        transition: color 0.3s ease;
        max-width: 260px;
    }

    &__price {
        font-size: 17px;
        font-weight: 700;
        min-width: 120px;
        text-align: right;
        margin-right: 20px;
    }

    &__link {
        color: $text-color;
        text-decoration: none;
    }

    &__column {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    &__column-row {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: flex-start;
    }

    &__tech-summary {
        display: flex;
    }

    &__tech-summary-column:first-child {
        width: 180px;
    }

    &__tech-summary-column:last-child {
        min-width: 80px;
    }

    &__cell {
        max-width: 180px;
        font-size: 15px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        color: $secondary-text-color;
        min-height: 1.25em;
    }

    &__additional-info {
        margin: 8px 0 0;
        font-size: 13px;
        color: $secondary-text-color;

        &_align_right {
            flex-grow: 1;
            text-align: right;
        }
    }

    &__year, &__mileage {
        font-size: 17px;
        margin-bottom: 8px;
    }

    &__year {
        min-width: 60px;
        text-align: left;
    }

    &__mileage {
        min-width: 100px;
        text-align: right;
    }

    &__clicker {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
    }
}

.card-m {
    padding: 20px;
    border-radius: 8px;
    background: $white;
    margin: 8px 0;
    box-shadow: 0 3px 14px $card-shadow-color;

    &__header {
        display: flex;
        flex-direction: column;
        margin-bottom: 12px;
    }

    &__title {
        font-size: 16px;
        font-weight: 400;
        line-height: 20px;
        margin: 0 0 2px;
    }

    &__price {
        font-size: 24px;
        font-weight: 700;
    }

    &__gallery {
        max-height: 65vw;
        display: flex;
        flex-wrap: wrap;
        flex-direction: column;
        overflow-x: auto;
        overflow-y: hidden;
        overscroll-behavior-x: contain;
        -webkit-overflow-scrolling: touch;
        scroll-snap-type: x mandatory;
        margin-top: 12px;
    }

    &__photo {
        overflow: hidden;
        scroll-snap-align: start;
        border-radius: 8px;
        margin-right: 2px;
        max-width: 100%;
        height: 100%;
        object-fit: contain;
    }

    &__params {
        font-size: 14px;
        display: flex;
        margin-top: 14px;
        margin-bottom: 12px;
    }

    &__params-column {
        flex: 1;
        min-width: 0;

        &:first-child .card-m__params-cell {
            padding-right: 12px;
        }
    }

    &__params-cell {
        overflow: hidden;
        margin: 4px 0;
        white-space: nowrap;
        text-overflow: ellipsis;
        min-height: 1.25em;

        &:first-child {
            margin-top: 0;
        }
    }

    &__footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #e0e0e0;
        padding-top: 14px;
    }

    &__location, &__source {
        font-size: 12px;
        color: grey;
    }
}
</style>
