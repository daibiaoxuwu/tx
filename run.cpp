#include "opencv2/core.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/highgui.hpp"
#include <stdio.h>
#include <stdlib.h>
using namespace cv;
  
Mat Bresenhamline(Mat pic,int x0,int y0,int x1,int y1,Vec3b color)
{
    /*
        x坐标:纵向 从上到下 y坐标:横向 从左到右
        输入:
        pic:    待处理Mat图片
        x0,y0:  直线起点的纵,横坐标
        x1,y1:  直线终点的纵,横坐标
        color:  Vec3b格式的RGB颜色
        返回值: 画好的Mat图片
    */
    int x,y,dx,dy;
    float k,e;

    if(x1<x0)
    {
        swap(x1,x0);
        swap(y1,y0);
    }

    dx=x1-x0; dy=y1-y0;
    
    if(dx==0)
    {
        for(int i=min(y0,y1);i<=max(y0,y1);++i)
            pic.at<Vec3b>(x1, i) = color;
        return pic;
    }


    k=float(dy)/dx;
    e=-0.5;
    x=x0;y=y0;

    if(dy>0)
        for(int i=0;i<=dx;++i)
        {
            pic.at<Vec3b>(x, y) = color;
            ++x;
            e+=k;
            while(e>=0)
            {
                ++y;
                if(e>=1) pic.at<Vec3b>(x, y) = color;
                --e;
            }
        }
    else
        for(int i=0;i<=dx;++i)
        {
            pic.at<Vec3b>(x, y) = color;
            ++x;
            e+=k;
            while(e<=-1)
            {
                --y;
                if(e<=-2) pic.at<Vec3b>(x, y) = color;
                ++e;
            }
        }
    return pic;
}

Mat MidPointCircle(Mat pic, int r,int x0, int y0, Vec3b color)
{
    /*
        x坐标:纵向 从上到下 y坐标:横向 从左到右
        输入:
        pic:    待处理图片矩阵
        r:      圆的半径
        x0,y0:  圆的圆心的纵,横坐标
        color:  Vec3b格式的RGB颜色
        返回值: 画好的Mat图片
    */
    pic.at<Vec3b>(x0, y0) = color;
    int x=0,y=r;
    float d=1.25;//+2*x0-y0;
    pic.at<Vec3b>(r+x0, y0) = color;
    pic.at<Vec3b>(x0, r+y0) = color;
    pic.at<Vec3b>(x0-r, y0) = color;
    pic.at<Vec3b>(x0, y0-r) = color;
    while(x<=y)
    {
        if(d<0)
            d+=2*x+3;
        else
            {d+=2*(x-y)+5;y--;}
        x++;
        pic.at<Vec3b>(x+x0, y+y0) = color;
        pic.at<Vec3b>(x0-x, y+y0) = color;
        pic.at<Vec3b>(x0-x, y0-y) = color;
        pic.at<Vec3b>(x+x0, y0-y) = color;
        pic.at<Vec3b>(y+x0, x+y0) = color;
        pic.at<Vec3b>(x0-y, x+y0) = color;
        pic.at<Vec3b>(x0-y, y0-x) = color;
        pic.at<Vec3b>(y+x0, y0-x) = color;
    }
    return pic;
}




int main()  
{  
    Mat picin = imread("1.jpg")
    //画一些直线(正方形部分)
    pic=Bresenhamline(pic, 0, 500, 500, 0,Vec3b(255,255,0));
    pic=Bresenhamline(pic, 1000, 500, 500, 0,Vec3b(255,255,0));
    pic=Bresenhamline(pic, 0, 500, 500, 1000,Vec3b(255,255,0));
    pic=Bresenhamline(pic, 1000, 500, 500, 1000,Vec3b(255,255,0));

    //画一些直线(斜线部分)
    pic=Bresenhamline(pic, 0, 1000, 500, 0,Vec3b(255,255,0));
    pic=Bresenhamline(pic, 0, 500, 1000, 1000,Vec3b(255,255,0));
    pic=Bresenhamline(pic, 1000, 0, 500, 1000,Vec3b(255,255,0));
    pic=Bresenhamline(pic, 1000, 500, 0, 0,Vec3b(255,255,0));

    //画一些直线(水平,竖直线部分)
    pic=Bresenhamline(pic, 0, 0, 500, 0,Vec3b(255,255,0));
    pic=Bresenhamline(pic, 1000, 1000, 500, 1000,Vec3b(255,255,0));
    pic=Bresenhamline(pic, 1000, 0, 1000, 500,Vec3b(255,255,0));
    pic=Bresenhamline(pic, 0, 1000, 0, 500,Vec3b(255,255,0));

    //画圆
    pic=MidPointCircle(pic, 200 ,500, 500, Vec3b(255,255,0));

    //展示图片
    imshow("picture", pic);  

    //等待按任意键
    waitKey();
    
    //输出到'output.jpg'
    imwrite("output.jpg",pic);  
    return 0;  
}  
