setWatch(function() {
  console.log("Pressed");
  showSmileyFace();
}, BTN1, {repeat:true, debounce:20, edge:"falling"});

function showFace() {
  console.log("Showing smiley face!");
  show("     \n"+
      " 1 1 \n"+
      "     \n"+
      "1   1\n"+
      " 111 \n");
  setTimeout(() => show(""), 1000);
}
