<template>
    <header class="header">
        <div class="container">
            <div class="header__container">
                <h1 class="header__logo" @click="clickLogo">
                    <router-link :to="{ name: 'Main Page' }" class="header__logo-link">
                        <svg viewBox="0 0 250 30" xmlns="http://www.w3.org/2000/svg">
                            <text x="11%" y="80%" class="header__logo-name">ISLE OF CARS</text>
                        </svg>
                    </router-link>
                </h1>
            </div>
        </div>
    </header>
</template>

<script>
import eventBus from '@/eventBus';

export default {
    name: 'TheHeader',
    methods: {
        clickLogo() {
            eventBus.$emit('reset-filters');
        },
    },
};
</script>

<style lang="scss" scoped>
@import '@/_vars';

.header {
    // background-color: $white;
    // padding: 24px 0;
    // margin: 10px 0;

    &__container {
        max-width: 920px;
        width: 100%;
        // display: flex;
        justify-content: space-between;
        text-align: center;
    }

    &__logo-link {
        // font-size: 110px;
        color: $black;
        font-family: $logo-font;
        color: $black;
        text-decoration: none;
    }
}

@media screen and (max-width: 1300px) {
    .header {
        &__container {
            margin-right: 0;
        }
    }
}

@media screen and (max-width: 1000px) {
    .header {
        width: 100%;
        justify-content: space-between;

        &__logo {
            width: auto;
            // font-size: 28px;
        }
    }
}

@media screen and (max-width: 480px) {
    .header {
        align-items: baseline;
    }
}

@media screen and (max-width: 350px) {
    .header {
        flex-direction: column;
    }
}
</style>
