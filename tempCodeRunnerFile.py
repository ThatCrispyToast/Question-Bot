elif message.content[1:] == 'rainbow':
            for i in range(10):
                await answer.edit(title='Rainbow', embed=discord.Embed(color=0x46019B))
                await asyncio.sleep(1)
                await answer.edit(title='Rainbow', embed=discord.Embed(color=0x007EFE))
                await asyncio.sleep(1)
                await answer.edit(title='Rainbow', embed=discord.Embed(color=0x00BB00))
                await asyncio.sleep(1)
                await answer.edit(title='Rainbow', embed=discord.Embed(color=0xFEF601))
                await asyncio.sleep(1)
                await answer.edit(title='Rainbow', embed=discord.Embed(color=0xDD0000))
                await asyncio.sleep(1)