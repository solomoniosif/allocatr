const path = require("path");
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  mode: "development",
  entry: { bundle: "./assets/scripts/index.js" },
  output: {
    filename: "[bundle].js",
    path: path.resolve(__dirname, "allocatr", "static", "js"),
  },
  module: {
    rules: [
      {
        test: /\.scss$/i,
        use: ["style-loader", "css-loader", "sass-loader"],
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  plugins: [
    new BundleAnalyzerPlugin()
  ]
};
