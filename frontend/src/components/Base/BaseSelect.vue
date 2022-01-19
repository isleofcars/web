<template>
    <div
        class="select-container"
        :class="[{'select-container_highlight': isInputFocused || !!selectedOption,
                'select-container__focused': isInputFocused,
                 'select-container__opened': showOptions,
                 'select-container__input_hover': isInputHover,
                'select-container__selected': !!selectedOption ,
        }]"
        v-click-outside="clickOutside"
    >
        <div
            class="select-container__select"
            :class="[{'select-container__has-chosen-value': userChoseOption,
                    'select-container_disabled': disabled,
                     'select-container__select_opened': showOptions,
                    'select-container__select_focused': isInputFocused},
                    `select-container__select_borders-${bordersType}`]"
            @click="onFocused()"
            @keyup.esc="resetSelections"
            @keyup.enter="enterPressed"
            @mouseover="isInputHover = true"
            @mouseout="isInputHover = false"
        >
            <template v-if="withInput">
                <input
                    class="input"
                    :class="{'disabled': disabled}"
                    type="text"
                    :placeholder="inputPlaceholder"
                    v-model="inputValue"
                    :disabled="disabled"
                    @input="showOptions = !disabled"
                    @focus="focusInput"
                    @blur="blurInput"
                    @keypress="isNumber"
                    ref="input"
                />

                <span
                    class="select-container__arrow"
                    :class="{'select-container__arrow_disabled': disabled}"
                    v-if="showChevron"
                >
                    <font-awesome-icon :icon="['fas', 'chevron-down']"/>
                </span>
            </template>
            <template v-else>
                <span class="select-container__value">
                    {{ `${this.valuePrependText}${this.selectedOption}` || placeholder }}
                </span>

                <span class="select-container__arrow rotate">
                    <font-awesome-icon
                        :class="{'rotate': true, 'rotate-up': showOptions}"
                        :icon="['fas', 'chevron-down']"
                    />
                </span>
            </template>
        </div>
        <transition name="options-fade">
            <ul class="select-container__options"
                v-if="showOptions"
                @mouseover="onHoverSelectList"
            >
                <li
                    v-if="!hideResetOption"
                    class="select-container__option"
                    @click="resetSelections"
                >
                    <font-awesome-icon class="select-container__icon" :icon="['fas', 'times']"/>
                    <span>{{ resetText }}</span>
                </li>
                <li
                    class="select-container__option"
                    v-for="(option, index) in filteredOptions"
                    :key="option"
                    @mousedown.prevent="selectOption(option)"
                >
                    <font-awesome-icon
                        v-if="option.length > 0"
                        class="select-container__icon"
                        :icon="['fas', 'check']"
                        v-visible="selectedOption === filteredOptions[index]"
                    />
                    <label class="select-container__label" v-if="option.length > 0">
                        <input type="checkbox" :value="option"/>
                        {{ option }}
                    </label>
                </li>
            </ul>
        </transition>
    </div>
</template>

<script>

import eventBus from '@/eventBus';

export default {
    name: 'BaseSelect',
    props: {
        options: {
            type: Array,
            required: true,
        },
        selectedOption: {
            type: String,
            default: '',
        },
        placeholder: {
            type: String,
            default: '',
        },
        withInput: {
            type: Boolean,
            default: false,
        },
        onlyNumbers: {
            type: Boolean,
            default: false,
        },
        disabled: {
            type: Boolean,
            default: false,
        },
        resetText: {
            type: String,
            default: 'Any',
        },
        bordersType: {
            type: String,
            default: 'all',
            validator: (value) => value === 'all' || value === 'left' || value === 'right',
        },
        hideResetOption: {
            type: Boolean,
            default: false,
        },
        valuePrependText: {
            type: String,
            default: '',
        },
        strictFilter: {
            type: Boolean,
            default: false,
        },
    },
    mounted() {
        eventBus.$on('clear-form', this.resetInput);
    },
    destroyed() {
        eventBus.$off('clear-form');
    },
    data() {
        return {
            isInputHover: false,
            isHoveredSelectList: false,
            showOptions: false,
            showChevron: true,
            id: Math.random(),
            inputValue: '',
            tempInputValue: '',
            userChoseOption: false,
            isInputFocused: false,
        };
    },
    computed: {
        filteredOptions() {
            if (!this.withInput) {
                return this.options;
            }
            if (this.userChoseOption && this.inputValue === this.selectedOption) {
                return this.options;
            }
            // console.log(this.options);
            // if user entered sth, we should autocomplete and suggest filtered options
            if (this.strictFilter) {
                return this.options.filter((option) => option.toLowerCase().startsWith(this.inputValue.toLowerCase()));
            }
            return this.options.filter((option) => option.toLowerCase().indexOf(this.inputValue.toLowerCase()) !== -1);
        },
        inputPlaceholder() {
            return this.tempInputValue || this.placeholder;
        },
    },
    methods: {
        selectOption(option) {
            this.userChoseOption = true;
            this.showOptions = false;
            if (option.length === 0) {
                this.userChoseOption = false;
            }
            this.clearHovered();
            this.$emit('selectOption', option);
            if (this.withInput) {
                // if user typed sth and then selected item from dropdown, set his selected to that value
                this.inputValue = option;
                this.tempInputValue = option;
                this.showChevron = true;
                this.$refs.input.blur();
            }
        },
        getRoot(e) {
            const current = e.target;
            let target;
            switch (current.tagName.toLowerCase()) {
            case 'span': {
                target = current.parentElement.parentElement;
                break;
            }
            case 'svg': {
                target = current.parentElement.parentElement;
                break;
            }
            case 'li': {
                target = current.parentElement;
                break;
            }
            case 'ul': {
                target = current;
                break;
            }
            case 'label': {
                target = current.parentElement.parentElement;
                break;
            }
            default:
                return undefined;
            }
            return target.parentElement;
        },
        onHoverSelectList(e) {
            const target = this.getRoot(e);
            const ADD = 'select-container__hovered';
            const toggle = 'select-container__opened';
            if (target !== undefined && target.classList.contains(toggle)) {
                const { nextSibling } = target;
                if (nextSibling !== null && !nextSibling.classList.contains(ADD)
                    && nextSibling.classList.contains('select-container__selected')) {
                    nextSibling.classList.add(ADD);
                }
                const { previousSibling } = target;
                if (previousSibling !== null && !previousSibling.classList.contains(ADD)
                    && previousSibling.classList.contains('select-container__selected')) {
                    previousSibling.classList.add(ADD);
                }
            }
        },
        onMouseOut(e) {
            const target = this.getRoot(e);
            const included = 'select-container__hovered';
            const toggle = 'select-container__opened';

            if (target !== undefined && target.classList.contains(toggle)) {
                const { nextSibling } = target;
                if (nextSibling !== null && nextSibling.classList.contains(included)) {
                    nextSibling.classList.remove(included);
                }
                const { previousSibling } = target;
                if (previousSibling !== null && previousSibling.classList.contains(included)) {
                    previousSibling.classList.remove(included);
                }
            }
        },
        onFocused() {
            this.showOptions = (this.disabled) ? false : !this.showOptions;
            if (!this.disabled) {
                this.clearHovered();
            }
        },
        resetSelections() {
            this.clearHovered();
            this.userChoseOption = false;
            this.showOptions = false;
            this.inputValue = '';
            this.tempInputValue = '';
            this.$emit('resetSelectedOptions');
        },
        focusInput() {
            if (this.disabled) return;
            this.clearHovered();
            this.isInputFocused = true;
            this.showChevron = false;
            if (this.userChoseOption) {
                this.tempInputValue = this.inputValue;
                this.inputValue = '';
            }
        },
        blurInput() {
            if (this.disabled) return;
            this.clearHovered();
            this.isInputFocused = false;
            this.showChevron = true;
            if (this.userChoseOption) {
                setTimeout(() => {
                    this.inputValue = this.tempInputValue;
                    this.tempInputValue = '';
                }, 200);
            }
        },
        clickOutside() {
            this.clearHovered();
            this.showOptions = false;
        },
        clearHovered() {
            const element = document.querySelector('.select-container__hovered');
            if (element !== null) {
                element.classList.remove('select-container__hovered');
            }
        },
        enterPressed() {
            if (!this.filteredOptions.length) return;
            this.selectOption(this.filteredOptions[0]);
        },
        resetInput() {
            this.inputValue = '';
        },
        isNumber(e) {
            if (!this.withInput || !this.onlyNumbers) return;
            const char = String.fromCharCode(e.keyCode);
            if (!(/\d/.test(char))) e.preventDefault();
        },
    },
    watch: {
        selectedOption(val) {
            this.selectOption(val);
        },
        inputValue(val) {
            const firstAutoComplete = this.filteredOptions[0];
            if (val === firstAutoComplete) {
                this.selectOption(firstAutoComplete);
            }
        },
    },
};
</script>

<style lang="scss" scoped>
@import '@/_vars.scss';
.select-container {
    position: relative;
    font-size: 15px;
    &:last-child {
        margin-left: -1px;
    }
    &:hover {
        z-index: 120;
    }
    &__focused {
        z-index: 110;
        &:hover {
            z-index: 115;
        }
    }
    &__select {
        height: 36px;
        background-color: $white;
        border: 1px solid rgba(0, 0, 0, .12);
        padding-left: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 110;
        &:hover {
            z-index: 15;
        }
        &__opened:hover {
            z-index: 110;
        }
        &:hover {
            border: 1px solid #157ee1;
            cursor: pointer;
            z-index: 110;
        }
        &ed {
            z-index: 112;
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
        }
    }
    &__selected {
        z-index: 113;
    }
    &__opened {
        z-index: 114;
        &:hover {
            z-index: 115;
        }
    }
    &__hovered {
        z-index: 115;
    }
    &__input_hover {
        z-index: 120 !important;
    }
    &__value {
        color: grey;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
    }
    &_disabled {
        border-color: rgba(0, 0, 0, .08);
        &:hover {
            cursor: default;
            border: 1px solid rgba(0, 0, 0, .08);
        }
    }
    &__has-chosen-value {
        border: 1px solid rgba(21, 126, 225, .5);
        background-color: #eef4fa;
        .select-container__value {
            color: $text-color;
        }
    }
    &__arrow {
        height: 100%;
        line-height: 36px;
        padding-right: 8px;
        opacity: .543;
        &_disabled {
            opacity: .2;
        }
    }
    &__options {
        position: absolute;
        width: 100%;
        z-index: 1500;
        margin-top: 10px;
        border-radius: 8px;
        background-color: $white;
        box-shadow: 0 10px 30px 0 rgb(0 0 0 / 10%);
        max-height: 250px;
        overflow: auto;
        overscroll-behavior: none;

        &:hover {
            .select-container {
                z-index: 1 !important;
            }
        }
    }
    &__option {
        display: flex;
        align-items: center;
        height: 36px;
        line-height: 36px;
        list-style-type: none;
        color: $text-color;
        padding-left: 8px;
        &:hover {
            cursor: pointer;
            color: $white;
            background-color: #157ee1;
        }
        &:hover * {
            opacity: 1;
        }

        input {
            display: none;
        }
    }
    &__icon {
        width: 15px;
        height: 15px;
        margin-right: 10px;
        opacity: .543;
    }
    &__label {
        width: 100%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        &:hover {
            cursor: pointer;
        }
    }
}
.input {
    outline: none;
    display: block;
    width: 100%;
    height: 100%;
    font-family: inherit;
    font-size: 15px;
    border: transparent;
    margin-right: 8px;
    background-color: inherit;
    color: #000;
    &:disabled::placeholder {
        color: rgba(0, 0, 0, .24);
    }
    &::placeholder {
        color: grey;
    }
}
.rotate {
    -moz-transition: all 0.1s linear;
    -webkit-transition: all 0.1s linear;
    transition: all 0.1s linear;
}
.rotate-up {
    transform-origin: center center;
    -ms-transform: rotate(-180deg);
    -moz-transform: rotate(-180deg);
    -webkit-transform: rotate(-180deg);
    transform: rotate(-180deg);
}
.options-fade-enter-active, .options-fade-leave-active {
    transition: opacity .5s;
}
.options-fade-enter, .options-fade-leave-to {
    opacity: 0;
}
</style>
