<template>
    <masonry
        :cols="{default: 6, 1000: 4, 700: 3, 400: 1}"
        :gutter="{default: 'var(--margin-main)', 700: '15px'}"
        >
        <template
            v-for="car in cars"
        >
            <AppCarCard
                :car="car"
                :key="`car-${car.id}`"
            />
        </template>
    </masonry>
</template>

<script>
import AppCarCard from '@/components/AppCarCard';

export default {
    name: 'AppCarsList',
    components: {
        AppCarCard,
    },
    props: {
        cars: {
            type: Array,
            required: true,
        },
    },
};
</script>
