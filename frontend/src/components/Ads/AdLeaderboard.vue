// Leaderboard ad template for AdSense (728x90)
<template>
    <div class="card">
        <div class="card__main">
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-format="fluid"
                 data-ad-layout-key="-fi-2o+7b-6y-2d"
                 data-ad-client="ca-pub-7888235063871015"
                 data-ad-slot="4028411827">
            </ins>
            <div v-el:script-holder></div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AdLeaderboard',
    ready() {
        const scriptEl = document.createElement('script');
        scriptEl.innerHTML = '(adsbygoogle = window.adsbygoogle || []).push({});';
        this.$els.scriptHolder.appendChild(scriptEl);
    },
};
</script>

<style lang="scss" scoped>
.ad {
    width: 728px;
    height: 90px;
    position: relative;
    background-color: lightgrey;

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
