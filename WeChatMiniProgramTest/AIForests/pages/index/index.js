// index.js
// 获取应用实例
const app = getApp()

Page({
  data: {
    motto: '请先上传图片',
    imageUrl: ''
  },
  uploadImage: function() {
    wx.chooseImage({
      count: 1,
      success: (res) => {
        const tempFilePath = res.tempFilePaths[0];
        this.setData({
          imageUrl: tempFilePath
        });
        wx.uploadFile({      
          url: 'https://cumtforests1.api.lymone.cc/predict',
          filePath: tempFilePath,
          name: 'image',
          success: function(res) {
            const data = JSON.parse(res.data);
            const result = data.result;
            this.setData({
              motto: result
            });
          },
          fail: function(error) {
            this.setData({
              motto: "上传失败请重试"
            });
          }
        });
    }
    })
  }
})