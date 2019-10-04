$('.dropdown-item').click(function(){
    $("#team-info").css("display", "none");
    var itemText = this.text;
    $("#team-name").text(itemText);
    $("#team-info").fadeIn();
})