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
            @blur="onBlur()"
            @keyup.enter="onBlur()"
            ref="input"
        />
    </div>
</template>

<script>
export default {
    name: 'BaseInput',
    props: {
        fromValue: {
            type: String,
            default: '0',
        },
        showUnits: {
            type: String,
            default: '',
        },
        placeholder: {
            type: String,
            default: '',
        },
        value: {
            type: String,
            required: true,
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
        fromValue(val) {
            // console.log('change another: ', val);
            const currentValue = Number(this.tempValue
                .replaceAll(',', '')
                .replaceAll(' ', '')
                .replaceAll(this.showUnits, ''));
            this.isError = currentValue < Number(val) && currentValue > 0;
        },
        isInputFocused(val) {
            if (this.showUnits === '') {
                return;
            }

            // Clear previous units
            this.tempValue = this.tempValue
                .replaceAll(this.showUnits, '')
                .replaceAll(' ', '');
            if (!val) {
                // Because it doesn't work otherwise.
                setTimeout(() => {
                    if (this.tempValue !== '') {
                        if (this.showUnits === '$') {
                            this.tempValue = `${this.showUnits}${this.tempValue}`;
                        } else {
                            this.tempValue += ` ${this.showUnits}`;
                        }
                    }
                }, 100);
            }
        },
        tempValue(val) {
            // console.log(`val: ${val}, number Error: ${this.fromValue}`);
            const currentValue = Number(val
                .replaceAll(',', '')
                .replaceAll(' ', '')
                .replaceAll(this.showUnits, ''));
            this.isError = currentValue < Number(this.fromValue) && currentValue > 0;
            // we don't update the value immediately to not send http request every time user types a letter
            // instead, we update the value 500ms after the user typed the last symbol
            if (!this.isInputFocused) {
                // For add unit
                return;
            }

            this.finishedTyping = false;
            clearTimeout(this.timeout);
            const onlyDigits = val.replace(/\D/g, '');
            if (!onlyDigits) {
                this.tempValue = '';
                this.finishedTyping = false; // we clean the filter
                return;
            }

            this.tempValue = new Intl.NumberFormat('en-US').format(onlyDigits);
            this.timeout = setTimeout(() => {
                if (!this.tempValue) return;
                this.finishedTyping = false;
            }, 700);
        },
        finishedTyping(val) {
            if (this.finishedTyping) {
                const temp = this.tempValue;
                if (temp !== null && temp.length > 0) {
                    this.isValueSelected = !!val;
                }
                const sendValue = temp
                    .replaceAll(',', '')
                    .replaceAll(' ', '')
                    .replaceAll(this.showUnits, '');
                if (val && !this.isError) {
                    this.$refs.input.blur();
                    this.$emit('input', sendValue);
                }
            }
        },
        value(val) {
            if (val !== this.tempValue.replaceAll(',', '')) {
                this.tempValue = val;
            }
            if (!val) {
                this.isValueSelected = false;
            }
        },
    },
    methods: {
        onBlur() {
            const { tempValue } = this;
            this.isInputFocused = false;
            if (tempValue !== null && tempValue.length > 0) {
                this.isValueSelected = true;
                this.finishedTyping = true;
            } else {
                this.isValueSelected = false;
                this.finishedTyping = true;
            }
        },
    },
};
</script>

<style lang="scss" scoped>
@import '@/_vars.scss';

.input-container {
    position: relative;
    font-size: 15px;
    // height: 36px;
    // background-color: $white;
    // border: 1px solid rgba(0, 0, 0, .12);
    // padding: 0 8px;

    &_selected {
        // border: 1px solid rgba(21, 126, 225, .5) !important;
        background-color: #eef4fa;
        z-index: 2;
    }
    &:hover,
    &_focused {
        cursor: text;
        // border: 1px solid #157ee1 !important;
        z-index: 10;
    }
    &_error {
        // border: 1px solid rgba(225, 21, 75, 0.5) !important;
        background-color: #ffdddd;
        z-index: 2;
    }
    &_borders-all {
        // border-radius: 8px;
    }
    &_borders-left {
        // border-top-left-radius: 8px;
        // border-bottom-left-radius: 8px;
    }
    &_borders-right {
        // border-top-right-radius: 8px;
        // border-bottom-right-radius: 8px;
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
