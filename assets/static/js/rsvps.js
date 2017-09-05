(function() {
    var containers = Object.create(null);
    var urls = [];
    document.querySelectorAll('.event__group').forEach(function(event) {
    var url;
    var link = event.querySelector('.event__group__link');
    var placeholder = event.querySelector('.event__group__rsvps');
    if (link && link.getAttribute('href') && placeholder) {
        url = link.getAttribute('href');
        containers[url] = placeholder;
        urls.push(url);
    }
    });
    var req = new XMLHttpRequest();
    var reqData = JSON.stringify({meetups: urls});
    req.open('POST', 'https://api.meet-the-meetups.org/rsvps/query', true);
    req.addEventListener("load", function() {
    var data = JSON.parse(this.responseText);
    Object.keys(data).forEach(function(url) {
        var info = data[url];
        var container = containers[url];
        if (!container || !info || !info.rsvp) {
        return;
        }
        container.innerHTML = '(' + info.rsvp.YesCount + ' RSVPs of max ' + info.rsvp.MaxCount + ')';
    });
    });
    req.send(reqData);
})();
