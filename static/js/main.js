function LibsViewModel() {
    var self = this;

    self.libsURI = 'http://localhost:5000/api/libs';
    self.username = "admin";
    self.password = "pass";
    self.libs = ko.observableArray();

    self.ajax = function(uri, method, data) {
        var request = {
            url: uri,
            type: method,
            contentType: "application/json",
            accepts: "application/json",
            cache: false,
            dataType: 'json',
            data: JSON.stringify(data),
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Basic " + btoa(self.username + ":" + self.password));
            },
            error: function(jqXHR) {
                console.log("ajax error " + jqXHR.status);
            }
        };
        return $.ajax(request);
    }

    self.beginAdd = function() {
        alert("Add");
    }
    self.beginEdit = function(lib) {
        alert("Edit: " + lib.title());
    }
    self.remove = function(lib) {
        alert("Remove: " + lib.title());
    }

    self.ajax(self.libsURI, 'GET').done(function(data) {
        for (var i = 0; i < data.libs.length; i++) {
            self.libs.push({
                uri: ko.observable(data.libs[i].uri),
                name: ko.observable(data.libs[i].Name),
                description: ko.observable(data.libs[i].Description),
                version: ko.observable(data.libs[i].Version)
            });
        }
    });
}
ko.applyBindings(new LibsViewModel());