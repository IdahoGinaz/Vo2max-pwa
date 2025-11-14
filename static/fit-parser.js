// Stubbed FitParser for testing load
(function (root) {
  function FitParser(options) {
    this.options = options || {};
  }

  // Fake parse method just returns a dummy structure
  FitParser.prototype.parse = function (arrayBuffer, callback) {
    const dummyData = {
      messages: [
        { name: "test_message", dummy_field: 123 }
      ]
    };
    callback(null, dummyData);
  };

  // Attach to window/global
  root.FitParser = FitParser;
})(typeof window !== "undefined" ? window : this);
