<template>
    <header class="header">
        <div class="container">
            <div class="header__container">
                <h1 class="header__logo" @click="clickLogo">
                    <router-link :to="{ name: 'Main Page', query: { page: 1 } }" class="header__logo-link">
                        <img class="header__logo-img" src="@/assets/logo.svg" alt="logo"/>
                        <span class="header__logo-name">ISLE OF CARS</span>
                    </router-link>
                </h1>
                <h2 class="header__motto">All cars in one place</h2>
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
    background-color: $accent-color;
    color: $white;
    font-family: $logo-font;
    padding: 24px 0;

    &__container {
        max-width: 920px;
        width: 100%;
        display: flex;
        justify-content: space-between;
    }

    &__logo {
        font-size: 32px;
        margin-right: 12px;
    }

    &__logo-img {
        width: 45px;
        height: 45px;
        vertical-align: text-bottom;
        margin-right: 8px;
    }

    &__logo-link {
        color: $white;
        text-decoration: none;
    }

    &__motto {
        font-size: 22px;
        flex-shrink: 0;
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
            font-size: 28px;
        }

        &__logo-img {
            width: 40px;
            height: 40px;
        }

        &__motto {
            font-size: 20px;
            margin: 0;
            transform: none;
        }
    }
}

@media screen and (max-width: 480px) {
    .header {
        align-items: baseline;

        &__logo {
            font-size: 22px;
        }

        &__logo-img {
            width: 35px;
            height: 35px;
        }

        &__motto {
            margin-top: 10px;
            font-size: 14px;
        }
    }
}

@media screen and (max-width: 350px) {
    .header {
        flex-direction: column;
    }
}
</style>
