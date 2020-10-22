// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Calculation on QR Code
******************************************************************************/

#include "..\Header\calculation_QR_code.h"

void printUsage(char** argv) {

	// Print usage
	cout << "Usage: " << argv[0] << " [-d <DEVICE>] [-w <CAPTUREWIDTH>] [-h <CAPTUREHEIGHT>]" << endl
		<< "Read QR code from given video device." << endl
		<< endl;

}

Point toCvPoint(Ref<zxing::ResultPoint> resultPoint) {
	return Point(resultPoint->getX(), resultPoint->getY());
}

//Read img name to scan the QR code inside
int ReadQRCode(Mat inputImage,const string mode) {

	if (!inputImage.data) {

		cout << "Could not open or find the image" << endl;
		return -1;
	}
	if (mode == "opencv"){

		// initialization
		QRCodeDetector qrDecoder = QRCodeDetector::QRCodeDetector();
		vector<Point> points;

		// detect and recognize QR code
		string data = qrDecoder.detectAndDecode(inputImage, points);

		if (data.length() > 0){

			// content of detected QR code
			cout << "Decoded Data: \n\n" << data << endl;

			// draw bouding box around QR code 
			//rectangle(inputImage, points[0], points[2], Scalar(0, 255, 0), 2);
			line(inputImage, points[0], points[1], Scalar(0, 255, 0), 2);
			line(inputImage, points[1], points[2], Scalar(0, 255, 0), 2);
			line(inputImage, points[2], points[3], Scalar(0, 255, 0), 2);
			line(inputImage, points[3], points[0], Scalar(0, 255, 0), 2);
		}
		else{

			cout << "WARNING: QR Code not detected" << endl;
		}
	}
	//if (mode == "zbar") {

	//	//¶¨ÒåÉ¨ÃèÆ÷
	//	ImageScanner scanner;
	//	scanner.set_config(ZBAR_NONE, ZBAR_CFG_ENABLE, 1);

	//	//Í¼Æ¬×ª»»
	//	Mat imageGray;
	//	cvtColor(inputImage, imageGray, CV_RGB2GRAY);
	//	int width = imageGray.cols;
	//	int height = imageGray.rows;
	//	uchar* raw = (uchar*)imageGray.data;

	//	Image imageZbar(width, height, "Y800", raw, width * height);
	//	scanner.scan(imageZbar); //É¨ÃèÌõÂë    
	//	Image::SymbolIterator symbol = imageZbar.symbol_begin();
	//	//É¨Ãè½á¹û´òÓ¡
	//	if (imageZbar.symbol_begin() == imageZbar.symbol_end())
	//	{
	//		cout << "²éÑ¯ÌõÂëÊ§°Ü£¬Çë¼ì²éÍ¼Æ¬£¡" << endl;
	//	}
	//	for (; symbol != imageZbar.symbol_end(); ++symbol)
	//	{
	//		cout << "ÀàÐÍ£º" << endl << symbol->get_type_name() << endl << endl;
	//		cout << "ÌõÂë£º" << endl << symbol->get_data() << endl << endl;
	//	}
	//	imageZbar.set_data(NULL, 0);//Çå³ý»º´æ
	//}
	if (mode == "zxing-cpp-master") {

		Mat img_gray;

		// Convert to grayscale
		cvtColor(inputImage, img_gray, CV_BGR2GRAY);

		try {

			// Create luminance  source
			Ref<LuminanceSource> source = MatSource::create(img_gray);

			// Search for QR code
			Ref<Reader> reader;
			reader.reset(new QRCodeReader);

			Ref<zxing::Binarizer> binarizer(new GlobalHistogramBinarizer(source));
			Ref<BinaryBitmap> bitmap(new BinaryBitmap(binarizer));
			Ref<zxing::Result> result(reader->decode(bitmap, zxing::DecodeHints(zxing::DecodeHints::TRYHARDER_HINT)));

			// Get result point count
			int resultPointCount = result->getResultPoints()->size();

			for (int j = 0; j < resultPointCount; j++) {

				// Draw circle
				circle(inputImage, toCvPoint(result->getResultPoints()[j]), 10, Scalar(110, 220, 0), 2);
			}
			// Draw boundary on image
			if (resultPointCount > 1) {

				for (int j = 0; j < resultPointCount; j++) {

					// Get start result point
					Ref<zxing::ResultPoint> previousResultPoint = (j > 0) ? result->getResultPoints()[j - 1] : result->getResultPoints()[resultPointCount - 1];

					// Draw line
					line(inputImage, toCvPoint(previousResultPoint), toCvPoint(result->getResultPoints()[j]), Scalar(110, 220, 0), 2, 8);

					// Update previous point
					previousResultPoint = result->getResultPoints()[j];
				}
			}
			if (resultPointCount > 0) {

				// Draw text
				//putText(inputImage, result->getText()->getText(), toCvPoint(result->getResultPoints()[0]), FONT_HERSHEY_PLAIN, 1, Scalar(110, 220, 0));
				cout << result->getText()->getText() << endl;
			}
		}
		catch (const ReaderException& e) {

			cerr << e.what() << " (ignoring)" << endl;
		}
		catch (const zxing::IllegalArgumentException& e) {

			cerr << e.what() << " (ignoring)" << endl;
		}
		catch (const zxing::Exception& e) {

			cerr << e.what() << " (ignoring)" << endl;
		}
		catch (const std::exception& e) {

			cerr << e.what() << " (ignoring)" << endl;
		}
	}
	namedWindow("Detected QR Code", 0);
	resizeWindow("Detected QR Code", 640, 480);
	imshow("Detected QR Code", inputImage);
	waitKey(2000);
	destroyWindow("Detected QR Code");
	return 0;
}