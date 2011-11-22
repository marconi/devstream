var streamItemData = [
    {
        "title": "The Quick",
        "content": "The quick brown fox jumps over the lazy dog!"
    },
    {
        "title": "Foo Bar",
        "content": "Aliquam aliquet, est a ullamcorper condimentum."
    }
];

/**
 * Models
 */

describe("StreamItem", function() {
    beforeEach(function() {
        this.streamItem = new StreamItem();
    });
    it("should be an instance of model", function() {
        expect(this.streamItem instanceof Backbone.Model).toBeTruthy();
    });
});

describe("StreamItemList", function() {
    beforeEach(function() {
        var streamItem = new StreamItem(streamItemData[0])
        this.streamItemList = new StreamItemList(streamItem);
    });
    it("should be an instance of collection", function() {
        expect(this.streamItemList instanceof Backbone.Collection).toBeTruthy();
    });
});

/**
 * Views
 */

describe("StreamItemView", function() {
    beforeEach(function() {
        var streamItem = new StreamItem(streamItemData[0])
        this.streamItemView = new StreamItemView({model: streamItem});
    });
    it("should be an instance of view", function() {
        expect(this.streamItemView instanceof Backbone.View).toBeTruthy();
    });
});

describe("StreamView", function() {
    beforeEach(function() {
        var c = new StreamItemList();
        for (var i=0; i<streamItemData.length; i++) {
            c.add(new StreamItem(streamItemData[i]));
        }
        this.streamView = new StreamView({collection: c});
    });
    it("it should be an instance of view", function() {
        expect(this.streamView instanceof Backbone.View).toBeTruthy();
    });
});

/**
 * Routers
 */

describe("Steam", function() {
    beforeEach(function() {
        this.stream = new Stream();
    });
    it("should be an instance of router", function() {
        expect(this.stream instanceof Backbone.Router).toBeTruthy();
    });
});
