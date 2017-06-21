

var rankingModule = (function () {

    var setRanking = function (el, score) {
        $(el).rating('rate', score);
    }


    return {
        setRanking: setRanking
    }

})();



