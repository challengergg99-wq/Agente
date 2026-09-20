import asyncio

async def dos_numeros(num1,num2,segundos):
    print(f"Los numeros son: {num1} y {num2} y se mostraran en {segundos} segundos")

    await asyncio.sleep(segundos)
    resultado = num1 + num2
    return resultado

async def main():
    resultados = await asyncio.gather(
        dos_numeros(5,10,2),
        dos_numeros(3,7,1)
    )

    print(f"resultados:{resultados}")

if __name__ == "__main__":    asyncio.run(main())