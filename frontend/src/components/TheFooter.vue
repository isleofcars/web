<template>
    <footer class="footer">
        <div class="container container-sm">
            <div class="footer__content">
                <ul class="footer__section">
                    <li>
                        We gathered all cars for sale in the US market to allow you easily find the best car to buy.
                    </li>
                </ul>
                <hr class="footer__section-divider"/>
                <ul class="footer__section">
                    <li>
                        All rights belong to their respective owners.
                        Isle of Cars is not responsible for the content published here.
                    </li>
                </ul>
            </div>
        </div>
    </footer>
</template>

<script>
export default {
    name: 'TheFooter',
};
</script>

<style lang="scss" scoped>
@import '@/_vars';

.footer {
    display: flex;
    flex-direction: column;
    gap: 12px;
    background-color: $footer-color;
    color: $footer-text-color;
    padding: 24px 5%;
    font-family: $logo-font;
    min-height: 177px;
    flex: 1 0 auto;

    &__content {
        width: 920px;
    }

    &__section {
        list-style-type: none;
        display: flex;
        gap: 16px;
        justify-content: space-around;
        margin: 20px 0;
        font-size: 18px;
        text-align: center;
    }

    &__section-divider {
        margin: 12px 5%;
        background-color: $divider-color;
        color: $divider-color;
        height: 1px;
        border: none;
    }

    &__icon {
        margin-right: 12px;
    }
}

@media screen and (max-width: 1300px) {
    .footer__content {
        margin: 0 auto;
    }
}

@media screen and (max-width: 1000px) {
    .footer {
        width: 100%;

        &__content {
            width: auto;
        }

        &__section {
            font-size: 16px;
            flex-direction: column;
        }
    }
}

@media screen and (max-width: 480px) {
    .footer__section {
        font-size: 14px;
    }
}
</style>
