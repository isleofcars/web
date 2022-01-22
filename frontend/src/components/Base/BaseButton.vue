<template>
    <button :class="[
                    'button',
                    `button_borders-${bordersType}`,
                ]"
            @click="onClick">
        <slot>Button</slot>
    </button>

</template>

<script>
export default {
    name: 'BaseFreeInput',
    props: {
        placeholder: {
            type: String,
            default: '',
        },
        bordersType: {
            type: String,
            default: 'all',
            validator: (value) => value === 'all' || value === 'left' || value === 'right',
        },
        onClick: {
            type: Function,
            required: true,
        },
    },
    data(props) {
        return {
            finishedTyping: false,
            timeout: null,
            tempValue: props.value,
            isInputFocused: false,
            isValueSelected: false,
            isError: false,
        };
    },
    watch: {
        tempValue(val) {
            this.$emit('input', val);
        },
    },
};
</script>

<style lang="scss" scoped>
@import '@/_vars.scss';

.button {
    position: relative;
    font-size: 15px;
    height: 36px;
    background-color: #157ee1;
    color: $white;
    border: 1px solid rgba(0, 0, 0, .12);
    padding: 0 8px;

    &:hover,
    &_focused {
        cursor: pointer;
        border: 1px solid #157ee1 !important;
        z-index: 10;
    }

    &_borders-all {
        border-radius: 8px;
    }

    &_borders-left {
        border-top-left-radius: 8px;
        border-bottom-left-radius: 8px;
    }

    &_borders-right {
        border-top-right-radius: 8px;
        border-bottom-right-radius: 8px;
        margin-left: -1px;
    }
}
</style>
