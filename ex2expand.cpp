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
int losswidth=5;

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
        //sum+= abs(picin.at<Vec3b>(i-1,j+1)[r] + 2*picin.at<Vec3b>(i,j+1)[r] + picin.at<Vec3b>(i+1,j+1)[r] - picin.at<Vec3b>(i-1,j-1)[r] - 2*picin.at<Vec3b>(i,j-1)[r] - picin.at<Vec3b>(i+1,j-1)[r]);
        //gradient
        //sum+= abs(picin.at<Vec3b>(i,j+1)[r] - picin.at<Vec3b>(i,j)[r]);
        //gradient2
        //sum+= abs(picin.at<Vec3b>(i,j+1)[r] - picin.at<Vec3b>(i,j-1)[r]);
        //laplace
        sum+=abs(picin.at<Vec3b>(i-1,j)[r] + picin.at<Vec3b>(i+1,j)[r] + picin.at<Vec3b>(i,j+1)[r] + picin.at<Vec3b>(i,j-1)[r] - 4*picin.at<Vec3b>(i,j)[r]);
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
	Mat picread = imread("1.jpg");
    int rows=picread.rows,cols=picread.cols;
    int csteps=picread.cols/3;
	Mat picin(picread.rows,picread.cols+csteps,CV_8UC3);
	for (int i = 0;i < rows;++i)
        for (int j = 0;j < cols;++j)
            for (int r = 0;r < 3;++r)
                picin.at<Vec3b>(i,j)[r]=picread.at<Vec3b>(i,j)[r];
	imshow("1.jpg",picin);
	waitKey();

    if(rotateFlag)
    {
        rotate(picin,90);
        rows=picread.cols;
        cols=picread.rows;
    }




//差值
    int** loss=newmat(rows,cols + csteps);

	for (int i = 1;i < rows-1;i++)
        for (int j = 1;j < cols-1;j++)
            loss[i][j]=diffcalc(picin,i,j);
//修正最后一行
    for (int i = 0;i < rows;i++)
    {
        loss[i][cols-1]=10000;
        loss[i][0]=10000;
    }
    for (int j = 0;j < cols + csteps;j++)
    {
        loss[rows-1][j]=10000;
        loss[0][j]=10000;
    }

    int** summ=newmat(rows,cols+csteps);
    int** last=newmat(rows,cols+csteps);
    for (int step = 0;step < csteps;step++)
    {
        //计算sum 动态规划
        for (int j = 0;j < cols+step;j++)
            summ[0][j]=0;
            //summ[0][j]=loss[0][j];
        for (int i = 0;i < rows-1;i++)
            for (int j = 0;j < cols+step;j++)
            {
                summ[i+1][j]=summ[i][max(j-1,0)];
                last[i+1][j]=max(j-1,0);
                for (int r = max(j-1,0)+1; r < min(j+2,cols-1+step); r++)
                {
                    if(summ[i][r]<summ[i+1][j]) //取三个的最小值
                    {
                        summ[i+1][j]=summ[i][r];
                        last[i+1][j]=r;                //存放上面一排的位置
                    }
                }
                summ[i+1][j]+=loss[i+1][j];
            }
                    
                    
        int minsum=10000000, oldm=0;
        //计算方差
        
            
        int* lineloss=new int[cols+step];
        memset(lineloss,0,(cols+step)*sizeof(int));
        
        for (int j = 1;j < cols-1+step;j++)
            for (int i = 1;i < rows-1;i++)
                lineloss[j]+=loss[i][j];

        double sum=0;
        for (int j = 1; j < cols-1+step; j++)   sum+=lineloss[j];
                
        double mean =  sum / (cols+step-2);
        double accum  = 0.0;  
        for (int j = 1; j < cols-1+step; j++)
            accum  += (lineloss[j]-mean)* (lineloss[j]-mean);
        double stdev = sqrt(accum/(cols+step-3))/mean/mean; //方差  
    
        for (int j = 1; j < cols-1+step; j++)        //因为第一列和最后一列没有,范围缩小,缩小掉黑边
            if(lineloss[j]<minsum)
            {
                minsum=lineloss[j];
                oldm=j;
            }
//            else printf("min:%d at %d; this %d at %d\n",minsum,oldm, lineloss[j],j);
        int minpos=oldm;
        printf("stdev: %lf mean: %lf min:%d minpos %d\n",stdev,mean, minsum, minpos);

//显示图片
/*
        Mat dst;
        picin.copyTo(dst);
        for (int i=rows-1;i>=0;--i)
        {
            for (int r=0;r<3;++r)
                dst.at<Vec3b>(i,minpos)[r]=0;
            minpos=last[i][minpos];                         //更新minpos
        }
        imshow("1.jpg",dst); waitKey(1);//pause
        minpos=oldm;
        */
        Mat dst;
        picin.copyTo(dst);
        for (int i=1;i<rows-1;++i)
        {
            int maxloss=0,maxpos=0;
            for (int j=1;j<cols-1+step;++j)
            {
                if(loss[i][j]>maxloss)  {maxloss=loss[i][j];maxpos=j;}
            }
//            printf("smallmax line %d value %d pos %d\n",i,maxloss,maxpos);
//            fflush(stdout);
            for (int j=1;j<cols-1+step;++j)
                for (int r=0;r<3;++r)
                    dst.at<Vec3b>(i,j)[r]=(255*loss[i][j])/maxloss;
        }
        imshow("1.jpg",dst); waitKey(1);//pause
        minpos=oldm;

/*
        Mat dst;
        picin.copyTo(dst);
        for (int i=1;i<rows-1;++i)
        {
            int maxsumm=0,maxpos=0;
            for (int j=1;j<cols-1;++j)
            {
                if(summ[i][j]>=10000)
                {
                    dst.at<Vec3b>(i,j)[0]=0;
                    dst.at<Vec3b>(i,j)[1]=0;
                    dst.at<Vec3b>(i,j)[2]=255;
                }
                else if(summ[i][j]>maxsumm)  {maxsumm=summ[i][j];maxpos=j;}
            }
            printf("smallmax line %d value %d pos %d\n",i,maxsumm,maxpos);
            fflush(stdout);
            for (int j=1;j<cols-1;++j)
                if(summ[i][j]<10000)
                    for (int r=0;r<3;++r)
                        dst.at<Vec3b>(i,j)[r]=(255*summ[i][j])/maxsumm;
        }
        imshow("1.jpg",dst); waitKey(1);
        minpos=oldm;
*/

        for (int i=rows-1; i>-1;i--)             //从最底下一直到最上面
        {
            for (int j=cols-1+step; j>minpos; j--)   //一行的像素左移
            {
                for (int r=0;r<3;++r)
                    picin.at<Vec3b>(i,j)[r]=picin.at<Vec3b>(i,j-1)[r];
                loss[i][j]=loss[i][j-1];                    //左移
            }
            minpos=last[i][minpos];                         //更新minpos
        }
        //更新loss
        minpos=oldm;
        for (int i=rows-1; i>0; i--)             //i不能从头到尾了因为计算loss i最后一行没有
        {
            int maxloss=0;
            for(int j=1;j<cols+step-1;++j) maxloss=max(maxloss,loss[i][j]);
            /*
            loss[i][minpos]=0;              //不能重复扩展
            loss[i][minpos+1]=10000;              //不能重复扩展
            for(int r=0; r<3; ++r)
                loss[i][minpos-1]+= abs(picin.at<Vec3b>(i,minpos+2)[r] - picin.at<Vec3b>(i,minpos)[r]);
                */
                //for(int j=max(0,minpos-losswidth);j<min(minpos+losswidth,cols+step);++j) loss[i][j]+=(maxloss*3/rows);
//                for(int j=max(0,minpos-losswidth);j<min(minpos+losswidth,cols+step);++j) loss[i][j]+=3;
            loss[i][minpos]+=2;
            loss[i][minpos+1]+=2;

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
    imshow("oldjpg",picread);
    waitKey();
	return 0;

}

















