#include "mvcam.h"
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <signal.h>
#include <string.h>

sig_atomic_t flag = 0;
void sigint_handler(int sig){
	flag = 1;
	printf("SIGINT\n");
}

void close_cam(dvpHandle *handle){
	dvpStatus dstat;
	mvCamStopTrigger(handle,&dstat);
	mvCamDestroy(handle,&dstat);

}

int main(){
	struct sigaction act;
	memset(&act,0,sizeof(struct sigaction));
	sigset_t mask;
	sigemptyset(&mask);
	act.sa_handler = sigint_handler;
	act.sa_mask = mask;
	act.sa_flags = 0;
	act.sa_sigaction = NULL;
	if(sigaction(SIGINT,&act,NULL) == -1){
		perror("sigaction:");
		exit(EXIT_FAILURE);
	}
	signal(SIGINT,sigint_handler);
	


	dvpHandle handle;
	dvpStatus dstat;
	mvStatus mstat;
	if((mstat = mvCamOpenDef(&handle,&dstat)) != MV_OK){
		fprintf(stderr,"UNABLE TO OPEN CAMERA\n");
		exit(EXIT_FAILURE);
	}

	mvExposure exp;
	memset(&exp,0,sizeof(mvExposure));
//	exp.mvexp_aflick = 0;
	exp.mvexp_shutter = 400;
//	exp.mvexp_aemode = 0;
//	exp.mvexp_aeop = 0;
//	exp.mvexp_aetarget = 0;
//	exp.mvexp_awop = 0;
	exp.mvexp_gain = 32.0;


	if((mstat = mvCamSetExposure(&handle,exp,&dstat)) != MV_OK){
		fprintf(stderr,"UNABLE TO SET EXPOSURE\n");
		close_cam(&handle);
		exit(EXIT_FAILURE);
	}


	if((mstat = mvCamStartTrigger(&handle,1.0,1.0,&dstat)) != MV_OK){
		fprintf(stderr,"UNABLE TO START TRIGGERING\n");
		close_cam(&handle);
		exit(EXIT_FAILURE);
	}
	mvCamImage img;
	int image_number =0;
	memset(&img,0,sizeof(mvCamImage));
	while(((mstat = mvCamGetImage(&handle,&img,5000,&dstat))==MV_OK)){
		image_number++;
		int num_bytes =snprintf(img.image_name,2048,"img%d.jpeg",image_number);
		img.image_name[num_bytes]='\0';
		if((mstat = mvCamSaveImage(&handle,&img,100,&dstat))!= MV_OK){
			fprintf(stderr,"UNABLE `SAVE IMAGE\n");
			close_cam(&handle);
			exit(EXIT_FAILURE);
		}
		memset(&img,0,sizeof(mvCamImage));
		printf("SAVED IMAGE %d\n",image_number);
		if(flag){
			mstat = MV_OK;
			break;
		}
	}

	if(mstat != MV_OK){
		fprintf(stderr,"UNABLE TO FETCH IMAGE\n");
		close_cam(&handle);
		exit(EXIT_FAILURE);		
	}	
	close_cam(&handle);

	


	exit(EXIT_SUCCESS);
}
