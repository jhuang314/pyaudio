$(function() {
  var interval = 10;
  var duration= 2000;
  var shake= 10;
  var vibrateIndex = 0;
  var selector = $('.face'); /* Your own container ID*/
    $(selector).click( /* The button ID */
    
    function(){ 

    vibrateIndex = setInterval(vibrate, interval);
    setTimeout(stopVibration, duration);
    
    });

    var vibrate = function(){
    $(selector).stop(true,false)
    .css({position: 'relative', 
    left: Math.round(Math.random() * shake) - ((shake + 1) / 2) +'px', 
    top: Math.round(Math.random() * shake) - ((shake + 1) / 2) +'px'
    });
    }
    
    var stopVibration = function() {
    clearInterval(vibrateIndex);
    $(selector).stop(true,false)
            .css({position: 'static', left: '0px', top: '0px'});
        };

    });