#include "myrplidar.h"


int main(int argc, const char * argv[]) {
	const char * opt_is_channel = NULL; 
	const char * opt_channel = NULL;
    const char * opt_channel_param_first = NULL;
	sl_u32         opt_channel_param_second = 0;
    sl_u32         baudrateArray[2] = {115200, 256000};
    sl_result     op_result;
	int          opt_channel_type = CHANNEL_TYPE_SERIALPORT;


	if(opt_channel_type == CHANNEL_TYPE_SERIALPORT)
	{
		if (!opt_channel_param_first) {
#ifdef _WIN32
		// use default com port
		opt_channel_param_first = "\\\\.\\com3";
#elif __APPLE__
		opt_channel_param_first = "/dev/tty.SLAB_USBtoUART";
#else
		opt_channel_param_first = "/dev/ttyUSB0";
#endif
		}
	}

    
    // create the driver instance
	ILidarDriver * drv = *createLidarDriver();

    if (!drv) {
        fprintf(stderr, "insufficent memory, exit\n");
        exit(-2);
    }



    // print out the device serial number, firmware and hardware version number..
    printf("SLAMTEC LIDAR S/N: ");
    for (int pos = 0; pos < 16 ;++pos) {
        printf("%02X", devinfo.serialnum[pos]);
    }

    printf("\n"
            "Firmware Ver: %d.%02d\n"
            "Hardware Rev: %d\n"
            , devinfo.firmware_version>>8
            , devinfo.firmware_version & 0xFF
            , (int)devinfo.hardware_version);



    // check health...
    if (!checkSLAMTECLIDARHealth(drv)) {
        goto on_finished;
    }

    signal(SIGINT, ctrlc);
    
	if(opt_channel_type == CHANNEL_TYPE_SERIALPORT)
        drv->setMotorSpeed();
    // start scan...
    drv->startScan(0,1);

    // fetech result and print it out...
    while (1) {
        sl_lidar_response_measurement_node_hq_t nodes[8192];
        size_t   count = _countof(nodes);

        op_result = drv->grabScanDataHq(nodes, count);

        if (SL_IS_OK(op_result)) {
            drv->ascendScanData(nodes, count);
            for (int pos = 0; pos < (int)count ; pos+=20) {
                printf("%s theta: %03.2f Dist: %08.2f Q: %d \n", 
                    (nodes[pos].flag & SL_LIDAR_RESP_HQ_FLAG_SYNCBIT) ?"S ":"  ", 
                    (nodes[pos].angle_z_q14 * 90.f) / 16384.f,
                    nodes[pos].dist_mm_q2/4.0f,
                    nodes[pos].quality >> SL_LIDAR_RESP_MEASUREMENT_QUALITY_SHIFT);
            }
        }

        if (ctrl_c_pressed){ 
            break;
        }
    }

    drv->stop();
	delay(200);
	if(opt_channel_type == CHANNEL_TYPE_SERIALPORT)
        drv->setMotorSpeed(0);
    // done!
on_finished:
    if(drv) {
        delete drv;
        drv = NULL;
    }
    return 0;
}

