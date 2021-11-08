<template>
    <div :class="['cookies-warning', {'cookies-warning__close': isClose}]">
        <p>
            This website uses cookies to personalize content and analyse
            traffic in order to offer you a better experience.
        </p>
        <button @click="closeWarning()">I accept and close</button>
    </div>
</template>

<script>
// import Vue from 'vue';
export default {
    name: 'CookiesWarning',
    data() {
        return {
            isClose: false,
        };
    },
    methods: {
        closeWarning() {
            this.isClose = true;
            localStorage.setItem('userAgreeCookies', 'true');
        },
    },
};
</script>

<style lang='scss' scoped>
@keyframes show_from_bottom {
    from {
        transform: translate(-50%, 150%);
    } to {
        transform: translate(-50%, 0%);
    }
}

@keyframes hide_to_bottom {
    from {
        transform: translate(-50%, 0%);
    } to {
        transform: translate(-50%, 150%);
    }
}

.cookies-warning {
    position: fixed;
    bottom: 15px;
    left: 50%;
    background: #fff;
    width: 70%;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    transform: translate(-50%, 150%);
    z-index: 99;
    padding: 30px;
    animation: show_from_bottom .5s 3s ease-in-out;
    animation-fill-mode: forwards, backwards;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 18px;

    &__close {
        animation: hide_to_bottom .7s ease-in-out;
        animation-fill-mode: forwards, backwards;
    }
    p {
        text-shadow: 0 0 5px rgba(0,0,0,.2)
    }
    button {
        color: #DB3727;
        border: none;
        border-bottom: 3px solid #DB3727;
        outline: none;
        background: none;
        font-size: 20px;
        font-weight: bold;
        display: block;
        transition: all .2s;
        cursor: pointer;
        min-width: 140px;
        margin-left: 20px;

        &:hover {
            transform: scale(1.06);
        }
    }
}

@media screen and (max-width: 1700px) {
    .cookies-warning {
        font-size: 16px;
        padding: 20px;

        button {
            font-size: 18px;
        }
    }
}

@media screen and (max-width: 1450px) {
    .cookies-warning {
        width: 75%;
    }
}

@media screen and (max-width: 1330px) {
    .cookies-warning {
        font-size: 14px;

        button {
            font-size: 16px;
        }
    }
}

    @media screen and (max-width: 1170px) {
    .cookies-warning {
        width: 80%;
    }
}

@media screen and (max-width: 700px) {
    .cookies-warning {
        flex-direction: column;
        width: 85%;

        p {
            text-align: center;
        }
        button {
            margin-top: 20px;
        }
    }
}

@media screen and (max-width: 500px) {
    .cookies-warning {
        width: 100%;
        bottom: 0;
        border-radius: 15px 15px 0 0;

        p {
            text-align: center;
        }
        button {
            margin-top: 20px;
        }
    }
}

@media screen and (max-width: 380px) {
    .cookies-warning {
        button {
            margin-top: 12px;
        }
    }
}
</style>
