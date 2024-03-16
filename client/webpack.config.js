const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: './src/index.js',
  mode: 'development',
  module: {
    rules: [
      {
         test: /\.(js|jsx)$/,
         exclude: /(node_modules)/,
         loader: 'babel-loader',
         options: { presets: ["@babel/env"]}
      },
      {
         test: /\.css$/,
         use:["style-loader", "css-loader"]
      }
    ]
  },
  resolve: { extensions: ['*','.js','.jsx']},
  output: {
    path: path.resolve(__dirname, 'dist/'),
    publicPath: '/dist/',
    filename: 'bundle.js'
  },
  devServer: {
    historyApiFallback: true,
    port: 3000,
    open: true,
    hot: true
  },
  plugins: [new webpack.HotModuleReplacementPlugin()]
}
