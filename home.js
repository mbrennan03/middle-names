$(document).ready(function () {
    generateMiddleName();
})

function generateMiddleName() {
    $('#generatorButton').click(function (event) {
        var nounType = Math.floor(Math.random() * 3);
        var noun = '';

        if (nounType == 0) {
            noun = 'Helium';
        } else if (nounType == 1) {
            noun = 'Aardvark';
        } else {
            noun = 'Banana';
        }

        var num = Math.floor((Math.random() * 19) + 1);

        var middleName = noun + ' - ' + num;

        $('#middleName').text(middleName);
    })
}