<template>
    <div class="filter__colours">
        <div class="colours">
            <div
                :class="['colour', colour, checkedColours.includes(colour) ? 'selected' : '']"
                @click="choiceColour(colour)"
                v-for="colour in mainColours"
                :key="colour"
            ></div>
        </div>
        <div class="filter__colours-reset" v-if="checkedColours.length > 0">
            <button
                @click="checkedColours = []"
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
            showAdditionalColours: false,
            checkedColours: [],
            mainColours: ['black', 'white', 'silver', 'blue', 'red', 'green', 'yellow', 'orange'],
        };
    },
    methods: {
        choiceColour(colour) {
            console.log(colour);
            if (this.checkedColours.includes(colour)) {
                const indexColour = this.checkedColours.indexOf(colour);
                this.checkedColours.splice(indexColour, 1);
            } else {
                this.checkedColours.push(colour);
            }
        },
        resetFilter() {
            this.checkedColours = [];
        },
    },
    watch: {
        checkedColours(val) {
            console.log(val);
            // and emmit to main in future...
        },
    },
};
</script>

<style lang='scss' scoped>
@import '@/_vars.scss';

.filter__colours {
    width: 280px;
    display: flex;
    justify-content: space-between;

    .colour {
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
    .filter__colours {
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
.silver {
    background-color: $silver;
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
