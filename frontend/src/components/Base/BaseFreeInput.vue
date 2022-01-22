<template>
    <div :class="[
                    'input-container',
                    { 'input-container_focused': isInputFocused,
                      'input-container_selected': isValueSelected,
                      'input-container_error': isError },
                    `input-container_borders-${bordersType}`,
                ]"
    >
        <input
            class="input-container__input"
            type="text"
            :placeholder="placeholder"
            v-model="tempValue"
            @focus="isInputFocused = true"
            ref="input"
        />
    </div>
</template>

<script>
export default {
    name: 'BaseFreeInput',
    props: {
        placeholder: {
            type: String,
            default: '',
        },
        value: {
            type: String,
            required: false,
        },
        bordersType: {
            type: String,
            default: 'all',
            validator: (value) => value === 'all' || value === 'left' || value === 'right',
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

.input-container {
    position: relative;
    font-size: 15px;
    height: 36px;
    background-color: $white;
    border: 1px solid rgba(0, 0, 0, .12);
    padding: 0 8px;
    &_selected {
        border: 1px solid rgba(21, 126, 225, .5) !important;
        background-color: #eef4fa;
        z-index: 2;
    }
    &:hover,
    &_focused {
        cursor: text;
        border: 1px solid #157ee1 !important;
        z-index: 10;
    }
    &_error {
        border: 1px solid rgba(225, 21, 75, 0.5) !important;
        background-color: #ffdddd;
        z-index: 2;
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
    &__input {
        outline: none;
        display: block;
        width: 100%;
        height: 100%;
        font-family: inherit;
        font-size: 15px;
        border: transparent;
        background-color: inherit;
        color: #000 !important;

        &::placeholder {
            color: grey !important;
        }
    }
}
</style>
