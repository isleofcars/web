// Mobile Leaderboard ad template for AdSense (320x50)
<template>
    <div class="ad">
        <p class="ad__text"></p>
    </div>
</template>

<script>
export default {
    name: 'AdMobileLeaderboard',
};
</script>

<style lang="scss" scoped>
.ad {
    width: 100%;
    height: 65vh;
    position: relative;
    background-color: lightgrey;
    margin: 8px 0;
    border-radius: 8px;

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

@media screen and (max-width: 580px ){
    .ad {
        height: 55vh;
    }
}

@media screen and (max-width: 470px ){
    .ad {
        height: 50vh;
    }
}

@media screen and (max-width: 410px ){
    .ad {
        height: 43vh;
    }
}
</style>
