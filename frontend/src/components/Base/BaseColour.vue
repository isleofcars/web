<template>
    <div class="filter__colours">
        <div class="colours">
            <div class="main-colours">
                <div
                    :class="['colour', colour, checkedColours.includes(colour) ? 'selected' : '']"
                    @click="choiceColour(colour)"
                    v-for="colour in mainColours"
                    :key="colour"
                ></div>
            </div>

            <div
                class="main-colours"
                v-show="showAdditionalColours"
            >
                <div
                    v-for="colour in additionalColours"
                    :key="colour"
                    :class="['colour', colour, checkedColours.includes(colour) ? 'selected' : '']"
                    @click="choiceColour(colour)"
                ></div>
            </div>
        </div>
        <div class="open-hidden-button">
            <button
                @click="showAdditionalColours = !showAdditionalColours"
                :class="showAdditionalColours ? 'active' : ''"
            ><font-awesome-icon :icon="['fas', 'chevron-down']"/>
            </button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'BaseColour',
    data() {
        return {
            showAdditionalColours: false,
            checkedColours: [],
            mainColours: [
                'black', 'silver-light', 'white', 'silver', 'blue',
                'orange-dark', 'green', 'brown', 'orange-light',
            ],
            additionalColours: [
                'blue-light', 'gold', 'red', 'purple',
                'yellow', 'coral', 'pink',
            ],
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
        margin-bottom: 6px;
        position: relative;

        &.selected::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            background: url("../../assets/checked_colour.svg");
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
        transform: rotate(0);
        transition: all .3s;

        &.active {
            transform: rotate(180deg);
        }
        .svg-inline--fa.fa-w-14 {
            width: 0.75em;
        }
        .svg-inline--fa {
            height: 1.6em;
        }
    }
}
.black {
    background: #000000;
}
.silver-light {
    background-color: $silver-light;
    background-image: linear-gradient(rgb(240, 240, 240), rgb(193, 193, 193));
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
.orange-dark {
    background-color: $orange-dark;
}
.green {
    background-color: $green;
}
.brown {
    background-color: $brown;
}
.orange-light {
    background-color: $orange-light;
}
.blue-light {
    background-color: $blue-light;
}
.gold {
    background-color: $gold;
    background-image: linear-gradient(rgb(255, 237, 2), rgb(253, 156, 0));
}
.red {
    background-color: $red;
}
.purple {
    background-color: $purple;
}
.yellow {
    background-color: $yellow;
}
.coral {
    background-color: $coral;
}
.pink {
    background-color: $pink;
}
</style>
