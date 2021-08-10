// Работа анимации перелистывания
//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

// Отработка нажатия на кнопку перехода к следующему вопросу
$(".next").click(function () {
    if (animating) return false;
    animating = true;

    current_fs = $(this).parent();
    next_fs = $(this).parent().next();

    //activate next step on progressbar using the index of next_fs
    // $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

    //show the next fieldset
    next_fs.show();
    //hide the current fieldset with style
    current_fs.animate({ opacity: 0 }, {
        step: function (now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale current_fs down to 80%
            scale = 1 - (1 - now) * 0.2;
            //2. bring next_fs from the right(50%)
            left = (now * 50) + "%";
            //3. increase opacity of next_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({
                'transform': 'scale(' + scale + ')',
                'position': 'absolute'
            });
            next_fs.css({ 'left': left, 'opacity': opacity });
        },
        duration: 800,
        complete: function () {
            current_fs.hide();
            animating = false;
        },
        //this comes from the custom easing plugin
        easing: 'easeInOutBack'
    });
});

// Отработка нажатия на кнопку возврата к предыдущему вопросу
$(".previous").click(function () {
    if (animating) return false;
    animating = true;

    current_fs = $(this).parent();
    previous_fs = $(this).parent().prev();

    //de-activate current step on progressbar
    // $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

    //show the previous fieldset
    previous_fs.show();
    //hide the current fieldset with style
    current_fs.animate({ opacity: 0 }, {
        step: function (now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale previous_fs from 80% to 100%
            scale = 0.8 + (1 - now) * 0.2;
            //2. take current_fs to the right(50%) - from 0%
            left = ((1 - now) * 50) + "%";
            //3. increase opacity of previous_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({ 'left': left });
            previous_fs.css({ 'transform': 'scale(' + scale + ')', 'opacity': opacity });
        },
        duration: 800,
        complete: function () {
            current_fs.hide();
            animating = false;
        },
        //this comes from the custom easing plugin
        easing: 'easeInOutBack'
    });
});

// Включение активности кнопки перехода к следующему тесту
$(".radio-btn").click(function () {
    // console.log($(this).parent().parent().parent().find(".next"))
    // $(this).parent().parent().parent().find(".action-button").removeClass("no-active");
    var el = $(this).parent();
    // console.log(el.prop('nodeName'));
    while(el.prop('nodeName') != "FIELDSET"){
        el = el.parent();
        // console.log(el.prop('nodeName'));
    }
    el.find(".action-button").removeClass("no-active");
})


// Включение чекбокса при нажатии на div блок
$(".answer").click(function () {
    $(this).find(".radio-btn").prop("checked", true);
    // console.log( $(this).find(".radio-btn"))
    $(this).find(".radio-btn").triggerHandler("click");
})

// Смена стиля оформления (выделение рамки) при тестировании по матрицам Равена
$(".content-img").click(function () {
    // Смена стиля оформления (выделение рамки)
    $(this).parent().parent().find(".selected").removeClass("selected");
    $(this).addClass("selected")
})

// Замер времени начала тестирования
var startTestingTime, endTestingTime
document.getElementById("start_test").addEventListener('click', () => {
    startTestingTime = new Date().getTime() / 1000;
    console.log(startTestingTime);
});

document.getElementById("end_test").addEventListener('click', () => {
    endTestingTime = new Date().getTime() / 1000;
    console.log(endTestingTime);
});


// Отправка на сервер ответов
var btn = document.getElementById('end_test');
btn.addEventListener('click', () => {
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    var formdata = new FormData();
    formdata.append("csrfmiddlewaretoken", csrf);
    formdata.append("start_testing_dtime", startTestingTime);
    formdata.append("end_testing_dtime", endTestingTime);

    let elements = document.querySelectorAll('input.radio-btn');
    var out_object = {};
    // перебираем элементы
    for (let elem of elements) {
        if (elem.checked) {
            // console.log(elem.name + "---" + elem.value);
            out_object[elem.name] = elem.value;
        }
    }

    formdata.append("data", JSON.stringify(out_object));

    var requestOptions = {
        method: 'POST',
        body: formdata,
        redirect: 'follow'
    };

    fetch(document.URL, requestOptions)
        .then(response => response.text())
        .then(result => {
            console.log(result);
            console.log('я делаю редирект');
            // document.location.href = window.location.origin + '/kettell_answers/' + result;
            document.location.href = window.location.origin;
        })
        .catch(error => console.log('error', error));
});





// ТАЙМЕР

var secondsRemaining;
var intervalHandle;

// function resetPage() {

//   document.getElementById("inputArea").style.display = "block";

// }

function tick() {
  // grab the h1
  var timeDisplay = document.getElementById("time");

  // turn the seconds into mm:ss
  var min = Math.floor(secondsRemaining / 60);
  var sec = secondsRemaining - (min * 60);

  //add a leading zero (as a string value) if seconds less than 10
  if (sec < 10) {
    sec = "0" + sec;
  }

  // concatenate with colon
  var message = min.toString() + ":" + sec;

  // now change the display
  timeDisplay.innerHTML = message;

  // stop is down to zero
  if (secondsRemaining === 0) {
    alert("Done!");
    clearInterval(intervalHandle);
    resetPage();
  }

  //subtract from seconds remaining
  secondsRemaining--;

}

document.getElementById("start_test").addEventListener('click', () => {
  // Включаем отображение таймера
  $("#time").removeClass("no-active");
// window.onload = function () {
// function startCountdown() {

  // function resetPage() {
  //   document.getElementById("inputArea").style.display = "block";
  // }

  // устанавливаем количество минут на таймере
  var minutes = Number(document.getElementById("time").innerHTML);
//   var minutes = 75;


  // // check if not a number
  // if (isNaN(minutes)) {
  //   alert("Please enter a number");
  //   return; // stops function if true
  // }

  // расчитываем кол-во секунд
  secondsRemaining = minutes * 60;

  //every second, call the "tick" function
  // have to make it into a variable so that you can stop the interval later!!!
  intervalHandle = setInterval(tick, 1000);

  // hide the form
  // document.getElementById("inputArea").style.display = "none";


});




// window.onload = function () {

//   // create input text box and give it an id of "min"
//   var inputMinutes = document.createElement("input");
//   inputMinutes.setAttribute("id", "minutes");
//   inputMinutes.setAttribute("type", "text");

//   //create a button
//   var startButton = document.createElement("input");
//   startButton.setAttribute("type", "button");
//   startButton.setAttribute("value", "Start Countdown");
//   startButton.onclick = function () {
//     startCountdown();
//   };

//   //add to the DOM, to the div called "inputArea"
//   document.getElementById("inputArea").appendChild(inputMinutes);
//   document.getElementById("inputArea").appendChild(startButton)

// }

// window.onload = () => {
//     var text = document.getElementById('burdon')

//     text.onse
// }
