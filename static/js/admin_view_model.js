//
//
//var view_model = function() {
//
//    var self = this;
//    this.spinner = '<i class="fas fa-lg fa-spinner fa-spin admin-update-spinner"></i>';
//    this.results = ko.observableArray();
//    this.surgeons_editable = ko.observableArray()
//    this.surgeons_editable_deleted = ko.observableArray()
//    this.current_surgeon = ko.observable();
//
//
//    this.checkbox_clicked = function() {
//        console.log("clicked")
//    }
//
//    this.update_languages = function(surgeon) {
//        var languages = $("#edit-languages").val()
//
//        $.post("/update_value", {surgeon_id: surgeon.id, column: "languages", languages: languages, csrf_token: window.csrf_token}, function(response) {
//            console.log(response)
//        })
//
//    }
//
//    this.update_latlng = function(surgeon) {
//
//        var latlng = $("#edit-latlng").val()
//
//        $.post("/update_value", {surgeon_id: surgeon.id, column: "latlng", latlng: latlng, csrf_token: window.csrf_token}, function(response) {
//            console.log(response)
//        })
//
//    }
//
//    this.update_locations = function(surgeon) {
//        var locations_col = $("#locations-row .location-col")
//
//        var locations = []
//
//        locations_col.each((i, v) => {
//
//            if (v) {
//                var title = $(v).find(".edit-location-title").val()
//                var addresses = $(v).find(".edit-location-address")
//
//                var formatted = []
//
//                if (addresses) {
//                    var addresses = addresses.each((i, value) => {
//                        var cv = $(value).val()
//
//                        if (cv) {
//                            formatted.push(cv)
//                        }
//                    })
//                }
//
//                next_object = {
//                    location_title: title,
//                    address: formatted.join("|")
//                }
//
//                locations.push(next_object)
//            }
//        })
//
//        $.post("/update_value", {surgeon_id: surgeon.id, column: "locations", locations: JSON.stringify(locations), csrf_token: window.csrf_token}, function(response) {
//            console.log(response)
//        })
//
//    }
//
//    this.restore_surgeon = function(surgeon) {
//
//        // self.add_loading()
//
//        $.post("/update_value", {surgeon_id: surgeon.id, column: "deleted", deleted: 0, csrf_token: window.csrf_token}, function(response) {
//            console.log(response)
//            if (response) {
//                var surg = self.surgeons_editable_deleted.remove((s) => {
//                    return s.id === surgeon.id
//                })[0];
//
//                self.surgeons_editable.push(surg)
//            }
//            // self.remove_loading()
//        })
//
//    }
//
//    this.delete_surgeon = function(surgeon) {
//
//        // self.add_loading()
//
//        $.post("/update_value", {surgeon_id: surgeon.id, column: "deleted", deleted: 1, csrf_token: window.csrf_token}, function(response) {
//            console.log(response)
//            if (response) {
//                var surg = self.surgeons_editable.remove((s) => {
//                    return s.id === surgeon.id
//                })[0];
//
//                self.surgeons_editable_deleted.push(surg)
//            }
//            // self.remove_loading()
//        })
//
//    }
//
//    this.update_title = function(surgeon) {
//        return function() {
//            var title = $("#edit-title").val()
//            console.log("updating Surgeon", surgeon)
//            self.add_loading()
//            $.post("/update_value", {surgeon_id: surgeon.id, column: "title", title: title, csrf_token: window.csrf_token}, function(response) {
//                console.log(response)
//                self.remove_loading()
//            })
//        }
//    }
//
//    this.update_phone = function(surgeon) {
//        return function() {
//            var phone = $("#edit-phone").val()
//            console.log("updating Surgeon", surgeon)
//            console.log(phone)
//
//            self.add_loading();
//
//            $.post("/update_value", {surgeon_id: surgeon.id, column: "phone",  phone: phone, csrf_token: window.csrf_token}, function(response) {
//                console.log(response)
//                self.remove_loading();
//            })
//        }
//    }
//
//    this.update_training = function(surgeon) {
//        return function() {
//
//            if (surgeon.training && surgeon.training.length > 0) {
//                var training_inputs = $(".edit-training")
//                var args = []
//
//                training_inputs.each((i, v) => {
//                    args.push(v.value)
//                })
//
//                var args = args.map(e => {
//                    return e.replace(",", "|")
//                })
//
//                surgeon.training = args
//
//                self.add_loading();
//
//                $.post("/update_value", {surgeon_id: surgeon.id, column: "training",  training: JSON.stringify(args), csrf_token: window.csrf_token}, function(response) {
//                    console.log(response)
//                    self.remove_loading();
//                })
//
//            } else {
//                console.log("No training to update")
//            }
//
//
//            // self.add_loading();
//            // $.post("/update_value", {surgeon_id: surgeon.id, column: "phone",  phone: phone, csrf_token: window.csrf_token}, function(response) {
//            //     console.log(response)
//            //     self.remove_loading();
//            // })
//        }
//    }
//
//
//    this.add_loading = function() {
//        $(".modal-title").append('<i class="fas fa-spinner fa-spin"></i>')
//    }
//
//    this.remove_loading = function() {
//        $(".modal-title .fa-spinner").remove()
//
//    }
//
//    this.create_copy = function(surgeon) {
//        var copy_obj = {}
//
//        for (var key in surgeon) {
//            copy_obj[key] = surgeon[key]
//        }
//
//        return copy_obj;
//    }
//
//
//    this.format_surgeon = function(surgeon) {
//        var surgeon_copy = this.create_copy(surgeon);
//
//        var training_json = JSON.parse(surgeon_copy.training);
//        var training_inputs = []
//
//        if (training_json) {
//            training_json.forEach(args => {
//
//                var split_args = args.split("|");
//                training_inputs.push(split_args);
//
//            })
//        }
//
//        surgeon_copy.training = training_inputs;
//
//        var locations = JSON.parse(surgeon_copy.locations);
//
//        var formatted_locations = []
//
//        locations = locations.map(l => {
//            if (l.address) {
//                l.address = l.address.split("|")
//                l.address = l.address.filter(v => {
//                    return v && v.length > 0
//                })
//            }
//
//            return l
//        })
//
//        surgeon_copy.locations = locations
//
//        return surgeon_copy;
//        // $.post("/admin/unique/latlng", {title: surgeon.title}, function(response) {
//        //     surgeon.latlng = surgeon.latlng.join("|")
//        //     surgeon.lat_lng_formatted
//        //     this.current_surgeon(surgeon)
//        // })
//    }
//
//    this.edit_surgeon = function(surgeon) {
//        var formatted = self.format_surgeon(surgeon);
//        self.current_surgeon(formatted)
//
//        $("#edit-surgeon-modal").modal();
//
//        var check = $("#the_checkbox")[0]
//
//        if (surgeon.uneditable) {
//            $(check).attr("checked", "checked")
//        }
//
//    }
//
//    this.load_surgeons = function(surgeon) {
//        // self.current_surgeon(surgeon)
//
//        $.post("/get_surgeons_by_title", {title: surgeon["title"], csrf_token: window.csrf_token}, function(surgeons) {
//            if (surgeons.surgeons_editable) {
//                self.surgeons_editable.removeAll()
//                surgeons.surgeons_editable.forEach(s => self.surgeons_editable.push(s))
//            }
//
//            if (surgeons.surgeons_editable_deleted) {
//                self.surgeons_editable_deleted.removeAll()
//                surgeons.surgeons_editable_deleted.forEach(s => self.surgeons_editable_deleted.push(s))
//            }
//
//            console.log(surgeons)
//        })
//
//        // console.log("Editing surgeon", surgeon)
//        // self.format_current_surgeon(surgeon)
//        // $("#edit-surgeon-modal").modal();
//    }
//
//    this.update_value = function(data) {
//        var parent = $(data).closest(".editable-value");
//        console.log(parent)
//        parent.find(".load-spinner").append(self.spinner)
//
//        window.setTimeout(function() {
//            parent.find(".load-spinner").empty();
//
//        }, 1000)
//    }
//
//    this.search = function() {
//
//        var search_value = $("#search").val();
//
//        console.log("Searching " + search_value)
//
//        jQuery.post('/admin/search', { search_value: search_value, csrf_token: window.csrf_token }, (data) => {
//            console.log(data)
//            if (data) {
//                self.results.removeAll();
//                // var surgeons = self.format_surgeons(data)
//                data.forEach((surgeon) => {
//                    self.results.push(surgeon)
//                })
//            }
//
//        })
//
//    }
//
//    // this.format_surgeons = function(surgeons) {
//    //     return surgeons.map(surgeon => {
//    //         surgeon.latlng
//    //     })
//    // }
//
//}
//
//view_model_instance = new view_model();
//
//var search_e = document.getElementById("search");
//
//search_e.addEventListener("keypress", function (e) {
//
//    if (e.code === "Enter") {
//
//        if (search_e.value.length > 0)
//
//            view_model_instance.search();
//
//    }
//
//});
//
//ko.applyBindings(view_model_instance);
