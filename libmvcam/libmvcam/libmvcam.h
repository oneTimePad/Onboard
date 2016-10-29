// The following ifdef block is the standard way of creating macros which make exporting 
// from a DLL simpler. All files within this DLL are compiled with the LIBMVCAM_EXPORTS
// symbol defined on the command line. This symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see 
// LIBMVCAM_API functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.



#ifndef MVCAM_H
#define MVCAM_H

#include "../DVPCamera/DVPCamera.h"
#include <string.h>


#define MAX_CAMERA_NAME 4095
#define MAX_IMAGE_NAME 4095
extern "C" {
	typedef struct _mvCamImage {
		dvpFrame frame;
		void *image_buffer;
		char image_name[MAX_IMAGE_NAME + 1];
		//telemetry goes here

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

	__declspec(dllexport) mvStatus mvCamOpen(char *camName, dvpHandle *handle, dvpStatus *ret_stat);
	__declspec(dllexport) mvStatus mvCamScan(char *output, int size, dvpStatus *ret_stat);
	__declspec(dllexport) mvStatus mvCamOpenDef(dvpHandle *handle, dvpStatus *ret_stat);
	__declspec(dllexport) mvStatus mvCamDestroy(dvpHandle *handle, dvpStatus *ret_stat);
	__declspec(dllexport) mvStatus mvCamStartTrigger(dvpHandle *handle, double delay, double loop, dvpStatus *ret_stat);
	__declspec(dllexport) mvStatus mvCamStopTrigger(dvpHandle *handle, dvpStatus *ret_stat);
	__declspec(dllexport) mvStatus mvCamGetImage(dvpHandle *handle, mvCamImage *image, dvpUint32 timeout, dvpStatus *ret_stat);
	__declspec(dllexport) mvStatus mvCamSaveImage(dvpHandle *handle, mvCamImage *image, int quality, dvpStatus *ret_stat);
	__declspec(dllexport) mvStatus mvCamSetExposure(dvpHandle *handle, mvExposure exp, dvpStatus *ret_stat);
}
#endif



/*
// This class is exported from the libmvcam.dll
class LIBMVCAM_API Clibmvcam {
public:
	Clibmvcam(void);
	// TODO: add your methods here.
};

extern LIBMVCAM_API int nlibmvcam;

LIBMVCAM_API int fnlibmvcam(void);
*/

