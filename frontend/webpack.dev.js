const path = require("path");
const { merge } = require("webpack-merge");
const common = require("./webpack.common.js");

module.exports = merge(common, {
  mode: "development",
  devServer: {
    historyApiFallback: true,
    port: 3000,
    open: true,
    hot: true,
    proxy: [
      {
        context: ["/api"],
        target: "http://localhost:8000",
        pathRewrite: { "^/api": "" },
      },
    ],
  },
});
