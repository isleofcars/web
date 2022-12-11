// Large Skyscraper ad template for AdSense (300x600)
<template>
    <div class="ad">
        <p class="ad__text"></p>
    </div>
</template>

<script>
export default {
    name: 'AdLargeSkyscraper',
};
</script>

<style lang="scss" scoped>
.ad {
    width: 0px;
    height: 0px;
    position: sticky;
    top: 20px;
    right: 0;
    background-color: lightgrey;
    flex-shrink: 0;
    display: none;

    &:hover {
        cursor: pointer;
    }

    &__text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 24px;
    }
}
</style>
