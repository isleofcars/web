// Leaderboard ad template for AdSense (728x90)
<template>
    <div class="card">
        <div class="card__main">
        </div>
    </div>
</template>

<script>
export default {
    name: 'AdLeaderboard',
};
</script>

<style lang="scss" scoped>
.ad {
    width: 728px;
    height: 90px;
    position: relative;
    background-color: lightgrey;
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
