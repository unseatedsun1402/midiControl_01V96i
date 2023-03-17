var slider = document.getElementById("my-slider");
var sliderValue = document.getElementById("slider-value");

sliderValue.innerHTML = slider.value;

slider.oninput = function() {
  sliderValue.innerHTML = this.value;
}
