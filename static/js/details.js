var gauge1 = Gauge(
    document.getElementById("gauge1"), {
      max: 150,
      dialStartAngle: -90,
      dialEndAngle: -90.001,
      value: 100,
      label: function(value) {
        return Math.round(value * 100) / 100;
      }
    }
  );
var gauge2 = Gauge(
    document.getElementById("gauge2"), {
      max: 150,
      dialStartAngle: -90,
      dialEndAngle: -90.001,
      value: 100,
      label: function(value) {
        return Math.round(value * 100) / 100;
      }
    }
  );
  (function loop() {

    gauge1.setValueAnimated(69, 1);
    gauge2.setValueAnimated(89, 1);
    window.setTimeout(loop, 6000);
  })();