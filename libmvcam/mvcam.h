


#ifndef MVCAM_H
#define MVCAM_H

#include "DVPCamera.h"
#include <string.h>


#define MAX_CAMERA_NAME 10000
#define MAX_IMAGE_NAME 4095
extern "C" {
	typedef enum { FALSE, TRUE} mybool;
	typedef struct _mvCamImage {
		dvpFrame frame;
		void *image_buffer;
		char image_name[MAX_IMAGE_NAME + 1];

	} mvCamImage;

	typedef struct _mvExposure {
		dvpAntiFlick    mvexp_aflick;
		double          mvexp_shutter;
		dvpAeMode       mvexp_aemode;
		dvpAeOperation  mvexp_aeop;
		dvpUint32	    mvexp_aetarget;
		dvpAwbOperation mvexp_awop;
		float			mvexp_gain;

	} mvExposure;

	typedef enum {
		MV_OK,
		MV_DVP_ERROR,
		MV_INVAL_ERROR,
		MV_NOMEM_ERROR,
		MV_NOCAM_ERROR,


	} mvStatus;

	mvStatus mvCamOpen(char *camName, dvpHandle *handle, dvpStatus *ret_stat);
	mvStatus mvCamScan(char *output, int size, dvpStatus *ret_stat);
	mvStatus mvCamOpenDef(dvpHandle *handle, dvpStatus *ret_stat);
	mvStatus mvCamDestroy(dvpHandle *handle, dvpStatus *ret_stat);
	mvStatus mvCamStartTrigger(dvpHandle *handle,  float loop, double delay, dvpStatus *ret_stat);
	mvStatus mvCamStopTrigger(dvpHandle *handle, dvpStatus *ret_stat);
	mvStatus mvCamGetImage(dvpHandle *handle, mvCamImage *image, dvpUint32 timeout, dvpStatus *ret_stat);
	mvStatus mvCamSaveImage(dvpHandle *handle, mvCamImage *image, int quality, dvpStatus *ret_stat);
	mvStatus mvCamSetExposure(dvpHandle *handle, mvExposure exp, dvpStatus *ret_stat);
}
#endif



