/* USER CODE BEGIN Header */
/**
  **************************
  * @file           : main.c
  * @brief          : Main program body
  **************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  **************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "math.h"
#include "stdio.h"
#include "stdlib.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c1;

UART_HandleTypeDef huart1;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_I2C1_Init(void);
static void MX_USART1_UART_Init(void);
/* USER CODE BEGIN PFP */
float Read_ADS1115(void);
void readADS1115Voltages(float *voltages, I2C_HandleTypeDef *hi2c, uint8_t address);

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

#define ADS1115_ADDRESS 0x48
//unsigned char ADSwrite[6];
//int16_t reading;
float voltage[4];
float adam_v=0;
int i,j = 0;
float toplam;

float current_voltage, speed_voltage, torque_voltage, batt_voltage;
float current, speed, torque, batt;
float electrical_power, mechanical_power, efficiency;


uint8_t Cmd_End[3] = {0xFF,0xFF,0xFF};  // command end sequence

void NEXTION_SendString (char *ID, char *string)
{
	char buf[50];
	int len = sprintf (buf, "%s.txt=\"%s\"", ID, string);
	HAL_UART_Transmit(&huart1, (uint8_t *)buf, len, 1000);
	HAL_UART_Transmit(&huart1, Cmd_End, 3, 100);
}

void NEXTION_SendNum (char *obj, int32_t num)
{
	uint8_t *buffer = malloc(30*sizeof (char));
	int len = sprintf ((char *)buffer, "%s.val=%ld", obj, num);
	HAL_UART_Transmit(&huart1, buffer, len, 1000);
	HAL_UART_Transmit(&huart1, Cmd_End, 3, 100);
	free(buffer);
}


void NEXTION_SendFloat (char *obj, float num, int dp)
{
	// convert to the integer
	int32_t number = num*(pow(10,dp));

	uint8_t *buffer = malloc(30*sizeof (char));
	int len = sprintf ((char *)buffer, "%s.vvs1=%d", obj, dp);
	HAL_UART_Transmit(&huart1, buffer, len, 1000);
	HAL_UART_Transmit(&huart1, Cmd_End, 3, 100);


	len = sprintf ((char *)buffer, "%s.val=%ld", obj, number);
	HAL_UART_Transmit(&huart1, buffer, len, 1000);
	HAL_UART_Transmit(&huart1, Cmd_End, 3, 100);
	free(buffer);
}

float custom_map(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_I2C1_Init();
  MX_USART1_UART_Init();
  /* USER CODE BEGIN 2 */

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

  readADS1115Voltages(voltage, &hi2c1, ADS1115_ADDRESS);
  HAL_Delay(10);

  //current_voltage = (voltage[0]);
  	    //current =(current_voltage - 2.500);
  	    //current_voltage = voltage[0]*3000;

  	   //current_voltage=((voltage[0]*9600)/20400)+voltage[0];
  	  	//current_voltage=current_voltage*1000;
  	    //current = (current_voltage-2440)/100-0.30;
  /*
  	  	for(int i=0;i<20;i++){
  	  	readADS1115Voltages(voltage, &hi2c1, ADS1115_ADDRESS);
  	  	voltage[0]=voltage[0]*1.0095;
  	  	toplam=toplam+voltage[0];
  	  	}
  	  	toplam=toplam/20;

        current_voltage=(toplam*9820)/19760 + toplam;
        current = (current_voltage-2.483)/0.04;
*/

  	    voltage[0]=voltage[0]*1.0075;
        //current_voltage=(voltage[0]*9820)/19760 + voltage[0];
        //current = (current_voltage-2.483)/0.04;
        i++;
        if(i!=20){
          	toplam=toplam+voltage[0];
        }
        else if(i==20){
        	toplam=toplam/20;
        	i=0;
        	current_voltage=(toplam*9820)/19760 + toplam;
        	current = (current_voltage-2.483)/0.04;
        }




  	    //speed_voltage = ((voltage[1]*20060)+(voltage[1]*9730))/9730;
  	    //speed_voltage = voltage[1]*3.054878048780488;
  	    speed_voltage = voltage[1]*1.5;
  	    speed = (speed_voltage*100);

  	    //torque_voltage = ((voltage[2]*9730)+(voltage[2]*20190))/20190;
  	    torque_voltage = voltage[2] ;
  	    torque = (torque_voltage*250)/5;

  	    //batt_voltage = ((voltage[3]*55120)+(voltage[3]*55120))/3220;
  	    batt_voltage = voltage[3]*38.65;
  	    batt = batt_voltage;

  	    electrical_power = current * batt_voltage;
  	    mechanical_power = ((speed*torque)/9549);
  	    efficiency = (mechanical_power/electrical_power)*100;


  	        NEXTION_SendFloat("x0", voltage[0],2);
  	  	    NEXTION_SendFloat("x4", voltage[1],2);
  	  	    NEXTION_SendFloat("x3", voltage[2],2);
  	  	    NEXTION_SendFloat("x2", voltage[3],2);
  	  	    NEXTION_SendFloat("x5", current,2);
  	  	    NEXTION_SendFloat("x8", speed,1);
  	  	    NEXTION_SendFloat("x7", torque,2);
  	  	    NEXTION_SendFloat("x6", batt,2);

  	  	    NEXTION_SendFloat("x9", electrical_power,2);
  	  	    NEXTION_SendFloat("x10", mechanical_power,2);
  	  	    NEXTION_SendFloat("x11", efficiency,2);
  }

  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV1;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief I2C1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_I2C1_Init(void)
{

  /* USER CODE BEGIN I2C1_Init 0 */

  /* USER CODE END I2C1_Init 0 */

  /* USER CODE BEGIN I2C1_Init 1 */

  /* USER CODE END I2C1_Init 1 */
  hi2c1.Instance = I2C1;
  hi2c1.Init.ClockSpeed = 100000;
  hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c1.Init.OwnAddress1 = 0;
  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c1.Init.OwnAddress2 = 0;
  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C1_Init 2 */

  /* USER CODE END I2C1_Init 2 */

}

/**
  * @brief USART1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART1_UART_Init(void)
{

  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 9600;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */

  /* USER CODE END USART1_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */
float Read_ADS1115 (void){

unsigned char buffer[3];
unsigned char i2c_addr= 0x90;
unsigned short data = 0;

			buffer[0] = 0x01;//adres pointer (0x01 config)
			buffer[1] = 0xC2;// A0 ±4.096V
			buffer[2] = 0xE5;
			HAL_I2C_Master_Transmit(&hi2c1,i2c_addr+0, (uint8_t*) buffer, 3,100);

			buffer[0] = 0x00;
			HAL_I2C_Master_Transmit(&hi2c1,i2c_addr+0, (uint8_t*)buffer, 1,100);
			HAL_I2C_Master_Receive (&hi2c1,i2c_addr+1,buffer,2,100);
			data= (buffer[0]<<8)+ buffer[1];
			if (data == 0xFFFF) data=0;

			return (float)(0.125 * (float) data);
}



void readADS1115Voltages(float *voltage, I2C_HandleTypeDef *hi2c, uint8_t address) {
	unsigned char ADSwrite[6];
    uint8_t ADSread[2];
    int16_t reading;

    for (int i = 0; i < 4; i++) {
        ADSwrite[0] = 0x01;
        switch (i) {
            case 0:
                ADSwrite[1] = 0xC2; // A0
                break;
            case 1:
                ADSwrite[1] = 0xD2; // A1
                break;
            case 2:
                ADSwrite[1] = 0xE2; // A2
                break;
            case 3:
                ADSwrite[1] = 0xF2; // A3
                break;
        }
        ADSwrite[2] = 0xE5; // PARAMETER SET
        HAL_I2C_Master_Transmit(hi2c, address << 1, ADSwrite, 3, 100);
        ADSwrite[0] = 0x00;

        HAL_I2C_Master_Transmit(hi2c, address << 1, ADSwrite, 1, 100);

        HAL_Delay(2);
        HAL_I2C_Master_Receive(hi2c, address << 1, ADSread, 2, 100);
        reading = (ADSread[0] << 8 | ADSread[1]);
        if (reading < 0) {
            reading = 0;
        }
		if (voltage[i] == 0xFFFF) voltage[i]=0;
        voltage[i] = reading * 0.000125;

    }
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */