function LibsViewModel() {
    var self = this;
    self.libs = ko.observableArray([
        {
            title: ko.observable('title #1'),
            description: ko.observable('description #1'),
            done: ko.observable(false)
        },
        {
            title: ko.observable('title #2'),
            description: ko.observable('description #2'),
            done: ko.observable(true)
        }
    ]);

    self.beginAdd = function() {
        alert("Add");
    }
    self.beginEdit = function(lib) {
        alert("Edit: " + lib.title());
    }
    self.remove = function(lib) {
        alert("Remove: " + lib.title());
    }
    self.markInProgress = function(lib) {
        lib.done(false);
    }
    self.markDone = function(lib) {
        lib.done(true);
    }
}
ko.applyBindings(new LibsViewModel());