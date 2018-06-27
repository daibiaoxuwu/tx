#include "opencv2/core.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/highgui.hpp"
#include <stdio.h>
#include <cmath>
#include <string>
#include <cstdlib>

using namespace cv;
using namespace std;
bool rotateFlag=false;

int** newmat(int rows, int cols)
{
    int** gray=new int*[rows];
	for (int i = 0;i < rows;i++)
        gray[i] = new int[cols];
    return gray;
}
int diffcalc(Mat picin, int i, int j)
{
    int sum=0;
    for(int r=0; r<3; ++r)
        //sobel
        //return abs(picin.at<Vec3b>(i-1,j+1)[r] + 2*picin.at<Vec3b>(i,j+1)[r] + picin.at<Vec3b>(i+1,j+1)[r] - picin.at<Vec3b>(i-1,j-1)[r] - 2*picin.at<Vec3b>(i,j-1)[r] - picin.at<Vec3b>(i+1,j-1)[r]);
        //gradient
        return abs(picin.at<Vec3b>(i,j+1)[r] - picin.at<Vec3b>(i,j)[r]);
        //gradient2
        //return abs(picin.at<Vec3b>(i,j+1)[r] - picin.at<Vec3b>(i,j-1)[r]);
        //laplace
        //sum+=abs(picin.at<Vec3b>(i-1,j)[r] + picin.at<Vec3b>(i+1,j)[r] + picin.at<Vec3b>(i,j+1)[r] + picin.at<Vec3b>(i,j-1)[r] - 4*picin.at<Vec3b>(i,j)[r]);
        //laplace2
        //sum+=abs(picin.at<Vec3b>(i-1,j-1)[r] + picin.at<Vec3b>(i-1,j)[r] + picin.at<Vec3b>(i-1,j+1)[r] + picin.at<Vec3b>(i,j-1)[r] - 8 * picin.at<Vec3b>(i,j)[r] + picin.at<Vec3b>(i,j+1)[r] + picin.at<Vec3b>(i+1,j-1)[r] + picin.at<Vec3b>(i+1,j)[r] + picin.at<Vec3b>(i+1,j+1)[r]);
    return sum;

}
void rotate(Mat& picin,double angle)
{
    cv::Point2f center(picin.cols / 2, picin.rows / 2);
    cv::Mat rot = cv::getRotationMatrix2D(center, angle, 1);
    cv::Rect bbox = cv::RotatedRect(center, picin.size(), angle).boundingRect();

    rot.at<double>(0, 2) += bbox.width / 2.0 - center.x;
    rot.at<double>(1, 2) += bbox.height / 2.0 - center.y;

    cv::warpAffine(picin, picin, rot, bbox.size());
    cv::imshow("1.jpg", picin);
    cv::waitKey(0);
    return;
}


int main()
{
	Mat picin = imread("1.jpg");
	imshow("1.jpg",picin);
	waitKey();
    int rows=picin.rows,cols=picin.cols;

    if(rotateFlag)
    {
        rotate(picin,90);
        rows=picin.rows,cols=picin.cols;
    }




//差值
    int** loss=newmat(rows,cols);

	for (int i = 1;i < rows-1;i++)
        for (int j = 1;j < cols-1;j++)
            loss[i][j]=diffcalc(picin,i,j);
//修正最后一行
    for (int i = 0;i < rows;i++)
    {
        loss[i][cols-1]=10000;
        loss[i][0]=10000;
    }
    for (int j = 0;j < cols;j++)
    {
        loss[rows-1][j]=10000;
        loss[0][j]=10000;
    }

    int** summ=newmat(rows,cols);
    int** last=newmat(rows,cols);
    for (int step = 0;step < cols/3;step++)
    {
        //计算sum 动态规划
        for (int j = 0;j < cols-step;j++)
            summ[0][j]=loss[0][j];
        for (int i = 0;i < rows-1;i++)
            for (int j = 0;j < cols-step;j++)
            {
                summ[i+1][j]=summ[i][max(j-1,0)];
                last[i+1][j]=max(j-1,0);
                for (int r = max(j-1,0)+1; r < min(j+2,cols-1-step); r++)
                {
                    if(summ[i][r]<summ[i+1][j]) //取三个的最小值
                    {
                        summ[i+1][j]=summ[i][r];
                        last[i+1][j]=r;                //存放上面一排的位置
                    }
                }
                summ[i+1][j]+=loss[i+1][j];
            }
                    
                    
        int minsum=100000, oldm=0;
        for (int j = 1; j < cols-1-step; j++)        //因为第一列和最后一列没有,范围缩小,缩小掉黑边
            if(summ[rows-1][j]<minsum)
            {
                minsum=summ[rows-1][j];
                oldm=j;
            }
        printf("min:%d %d\n",minsum, oldm);
        int minpos=oldm;

//显示图片
/*
        for (int i=rows-1;i>-1;i--)
        {
            for (int r=0;r<3;++r)
                picin.at<Vec3b>(i,minpos)[r]=0;
            minpos=last[i][minpos];
        }
        
        imshow("1.jpg",picin); waitKey(0);
        minpos=oldm;
*/
        for (int i=rows-1; i>-1;i--)             //从最底下一直到最上面
        {
            for (int j=minpos; j<cols-1-step;j++)   //一行的像素左移
            {
                for (int r=0;r<3;++r)
                    picin.at<Vec3b>(i,j)[r]=picin.at<Vec3b>(i,j+1)[r];
                loss[i][j]=loss[i][j+1];                    //左移
            }
            for (int r=0;r<3;++r)
                picin.at<Vec3b>(i,cols-1-step)[r]=0;//最左边抹黑
            minpos=last[i][minpos];                         //更新minpos
        }
        //更新loss
        minpos=oldm;
        for (int i=rows-1; i>0; i--)             //i不能从头到尾了因为计算loss i最后一行没有
        {
            loss[i][minpos]=diffcalc(picin,i,minpos);
            minpos=last[i][minpos];                         //更新minpos
        }
        printf("%d\n",step);
        fflush(stdout);
        /*
        char s[10];
        sprintf(s,"b%d.jpg",step);
        imwrite(s,picin);

        imshow("1.jpg",picin);
        waitKey();
*/
    }
    if(rotateFlag) rotate(picin,-90);
    imshow("1.jpg",picin);
    waitKey();
	return 0;

}

















