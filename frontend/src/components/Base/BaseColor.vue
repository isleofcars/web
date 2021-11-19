<template>
    <div class="filter__colors">
        <div class="colors">
            <div
                :class="['color', color, checkedColors.includes(color) ? 'selected' : '']"
                @click="choiceColor(color)"
                v-for="color in colors"
                :key="color"
            ></div>
        </div>
        <div class="filter__colors-reset" v-visible="checkedColors.length > 0">
            <button
                @click="checkedColors = []"
            ><font-awesome-icon :icon="['fas', 'times']"/>
            </button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'BaseColor',
    data() {
        return {
            showAdditionalColors: false,
            checkedColors: [],
            colors: ['black', 'white', 'gray', 'blue', 'red', 'green', 'yellow', 'orange'],
        };
    },
    methods: {
        choiceColor(color) {
            if (this.checkedColors.includes(color)) {
                const indexColor = this.checkedColors.indexOf(color);
                this.checkedColors.splice(indexColor, 1);
            } else {
                this.checkedColors.push(color);
            }
        },
        resetFilter() {
            this.checkedColors = [];
        },
    },
    watch: {
        checkedColors(val) {
            this.$emit('changeColors', val);
        },
    },
};
</script>

<style lang='scss' scoped>
@import '@/_vars.scss';

.filter__colors {
    width: 280px;
    display: flex;
    justify-content: space-between;

    .color {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        cursor: pointer;
        margin-right: 8px;
        position: relative;

        &.selected::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            background: url("../../assets/checked_color.svg");
            z-index: 999;
            display: inline-block;
            height: 20px;
            width: 20px;
            border-radius: 50%;
        }
    }
    button {
        background: none;
        border: none;
        outline: none;
        border-radius: 50%;
        box-shadow: 0 0 2px rgba(0,0,0,0.4);
        display: inline-block;
        height: 20px;
        width: 20px;
        cursor: pointer;
        font-size: 12px;
        line-height: 10px;
    }
}

@media screen and (max-width: 1000px) {
    .filter__colors {
        width: 100%;
    }
}

.black {
    background: #000000;
}
.white {
    background: #ffffff;
    box-shadow: inset 0 0 0 1px #e0e0e0;
}
.gray {
    background-color: $gray;
}
.blue {
    background-color: $blue;
}
.orange {
    background-color: $orange;
}
.green {
    background-color: $green;
}
.red {
    background-color: $red;
}
.yellow {
    background-color: $yellow;
}
</style>
