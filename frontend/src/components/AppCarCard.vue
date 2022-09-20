<template>
    <div class="card">
        <div class="card-m__gallery" v-if="photosLoaded">
            <img
                class="card__photo"
                v-for="(photo, index) in previewPhotos"
                :key="index"
                :src="getPhoto(index)"
            />
        </div>
        <div v-else class="card-m__gallery">
            <content-placeholders :rounded="true">
                <content-placeholders-img class="card__photo" />
                <content-placeholders-img class="card__photo" />
                <content-placeholders-img class="card__photo" />
            </content-placeholders>
        </div>

        <div class="card__description">
            <p>
                <span class="card__title">
                    {{ title }}
                    <span v-if="car !== 0"> {{ car.year }}</span>
                </span>
                <span>&nbsp;–&nbsp;</span>
                <span>
                    {{ power }} {{ transmission }} {{ mileage }} {{ drive }} {{ body }} {{ car.location }}
                </span>
            </p>
            <div class="card__footer">
                <a :href="car.url" class="card__link" target="_blank" rel="noreferrer">
                    View on {{ car.source }}
                </a>
                <h3 class="card__price">
                    {{ price }}
                </h3>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'AppCarCard',
    components: {},
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
                return '';
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
            if (this.car.photos) return this.car.photos.slice(0, 1);
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

.card {
    // width: 100%;
    position: relative;
    // padding: 16px;
    // background-color: $white;
    z-index: 1;
    margin-bottom: var(--margin-main);

    &:hover {
        z-index: 2;
        // border-radius: 8px;
        // background-color: #fff;
        // box-shadow: 0 5px 20px 0 $card-shadow-color;
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
        // border-radius: 8px;
    }

    &__description {
        // display: flex;
        // padding: 0 16px;
        // justify-content: space-between;
        width: 100%;
    }

    &__title {
        // font-size: 17px;
        font-weight: 700;
        transition: color 0.3s ease;
        max-width: 260px;
    }

    &__price {
        font-weight: 700;
        text-align: right;
        word-break: keep-all;
        line-height: 1rem;
    }

    &__link {
        // font-size: 12px;
        color: grey;
        font-size: 0.75rem;
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

    &__photo {
        opacity: 0.9;
        overflow: hidden;
        scroll-snap-align: start;
        // border-radius: 8px;
        // margin-right: 2px;
        max-width: 100%;
        height: 100%;
        object-fit: contain;
    }

    &__footer {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }
}

.card-m {
    padding: 20px;
    // border-radius: 8px;
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
        // margin-top: 12px;
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
