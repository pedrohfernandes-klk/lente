(function () {
  'use strict';

  var EPILente = window.EPILente || {};

  EPILente.safeStorage = {
    get: function (key) {
      try {
        var value = window.localStorage.getItem(key);
        return value === null ? null : value;
      } catch (error) {
        return null;
      }
    },
    set: function (key, value) {
      try {
        window.localStorage.setItem(key, value);
        return true;
      } catch (error) {
        return false;
      }
    },
    remove: function (key) {
      try {
        window.localStorage.removeItem(key);
        return true;
      } catch (error) {
        return false;
      }
    }
  };

  EPILente.getFocusable = function (root) {
    if (!root) root = document;
    var selector = [
      'a[href]',
      'button:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      'textarea:not([disabled])',
      '[tabindex]:not([tabindex="-1"])',
      '[contenteditable="true"]'
    ].join(',');
    return Array.prototype.filter.call(root.querySelectorAll(selector), function (element) {
      return !!(element.offsetWidth || element.offsetHeight || element.getClientRects().length);
    });
  };

  EPILente.focusFirst = function (root) {
    var focusable = EPILente.getFocusable(root);
    if (!focusable.length) return false;
    try {
      focusable[0].focus();
      return true;
    } catch (error) {
      return false;
    }
  };

  window.EPILente = EPILente;
}());
