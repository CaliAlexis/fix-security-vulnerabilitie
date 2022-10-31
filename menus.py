import discord


class Setup(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.value = None
        self.user_id = user_id

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='All', style=discord.ButtonStyle.green)
    async def all(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        self.value = 'all'
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Punishments', style=discord.ButtonStyle.blurple)
    async def punishments(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        self.value = 'punishments'
        self.stop()

    @discord.ui.button(label='Staff Management', style=discord.ButtonStyle.blurple)
    async def staff_management(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        self.value = 'staff management'
        self.stop()

    @discord.ui.button(label='Shift Management', style=discord.ButtonStyle.blurple)
    async def shift_management(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        self.value = 'shift management'
        self.stop()


class Dropdown(discord.ui.Select):
    def __init__(self, user_id):
        self.user_id = user_id
        options = [
            discord.SelectOption(
                label="Staff Management",
                value="staff_management",
                description="Inactivity Notices, and managing staff members"
            ),
            discord.SelectOption(
                label="Anti-ping",
                value="antiping",
                description="Responding to certain pings, ping immunity"
            ),
            discord.SelectOption(
                label="Punishments",
                value="punishments",
                description="Punishing community members for rule infractions"
            ),
            discord.SelectOption(
                label="Shift Management",
                value="shift_management",
                description="Shifts (duty on, duty off), and where logs should go"
            ),
            discord.SelectOption(
                label="Verification",
                value="verification",
                description="Currently in active development"
            ),
            discord.SelectOption(
                label="Customisation",
                value="customisation",
                description="Colours, branding, prefix, to customise to your liking"
            )
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select a category', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.user_id:
            await interaction.response.defer()
            self.view.value = self.values[0]
            self.view.stop()


class CustomDropdown(discord.ui.Select):
    def __init__(self, user_id, options: list):
        self.user_id = user_id
        optionList = []

        for option in options:
            optionList.append(
                discord.SelectOption(
                    label=option.replace('_', ' ').title(),
                    value=option
                )
            )

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select an option', min_values=1, max_values=1, options=optionList)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.user_id:
            await interaction.response.defer()
            self.view.value = self.values[0]
            self.view.stop()


class SettingsSelectMenu(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.value = None
        self.user_id = user_id

        self.add_item(Dropdown(self.user_id))


class YesNoMenu(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.value = None
        self.user_id = user_id

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        self.value = True
        await interaction.edit_original_response(view=self)
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='No', style=discord.ButtonStyle.danger)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        self.value = False
        await interaction.edit_original_response(view=self)
        self.stop()


class ShiftModify(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.value = None
        self.user_id = user_id

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Add time (+)', style=discord.ButtonStyle.green)
    async def add(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        self.value = "add"
        await interaction.edit_original_response(view=self)
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Remove time (-)', style=discord.ButtonStyle.danger)
    async def remove(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        self.value = "remove"
        await interaction.edit_original_response(view=self)
        self.stop()

    @discord.ui.button(label='End shift', style=discord.ButtonStyle.danger)
    async def end(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        self.value = "end"
        await interaction.edit_original_response(view=self)
        self.stop()

    @discord.ui.button(label='Void shift', style=discord.ButtonStyle.danger)
    async def void(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        self.value = "void"
        await interaction.edit_original_response(view=self)
        self.stop()
class LOAMenu(discord.ui.View):
    def __init__(self, bot, roles, loa_role, user_id):
        super().__init__()
        self.value = None
        self.bot = bot
        if isinstance(roles, list):
            self.roles = roles
        elif isinstance(roles, int):
            self.roles = [roles]
        self.loa_role = loa_role
        self.user_id = user_id



    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Accept', style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        for role in self.roles:
            if role in [role.id for role in interaction.user.roles]:
                await interaction.response.defer()
                for item in self.children:
                    item.disabled = True
                    if item.label == 'Deny':
                        self.children.remove(item)
                    if item.label == "Accept":
                        item.name = "Accepted"


                s_loa = None
                for loa in await self.bot.loas.get_all():
                    if loa['message_id'] == interaction.message.id and loa['guild_id'] == interaction.guild.id:
                        s_loa = loa

                try:
                    s_loa['accepted'] = True
                    guild = self.bot.get_guild(s_loa['guild_id'])
                    user = guild.get_member(s_loa['user_id'])
                    success = discord.Embed(
                        title=f"<:CheckIcon:1035018951043842088> {s_loa['type']} Accepted",
                        description=f"<:ArrowRightW:1035023450592514048> {interaction.user.mention} has accepted your {s_loa['type']} request.",
                        color=0x71c15f
                    )
                    await user.send(embed=success)
                    await self.bot.loas.update_by_id(s_loa)
                    role = discord.utils.get(interaction.guild.roles, id=self.loa_role)
                    if role is not None:
                        await user.add_roles(role)
                except:
                    pass
                self.value = True
                await interaction.edit_original_response(view=self)
                self.stop()
                continue

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Deny', style=discord.ButtonStyle.danger)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        for role in self.roles:
            if role in [role.id for role in interaction.user.roles]:
                await interaction.response.defer()
                for item in self.children:
                    item.disabled = True
                    if item.label == 'Accept':
                        self.children.remove(item)
                    if item.label == "Deny":
                        item.name = "Denied"

                s_loa = None
                for loa in await self.bot.loas.get_all():
                    if loa['message_id'] == interaction.message.id and loa['guild_id'] == interaction.guild.id:
                        s_loa = loa

                try:
                    s_loa['denied'] = True
                    guild = self.bot.get_guild(s_loa['guild_id'])
                    user = guild.get_member(s_loa['user_id'])
                    success = discord.Embed(
                        title=f"<:ErrorIcon:1035000018165321808> {s_loa['type']} Denied",
                        description=f"<:ArrowRightW:1035023450592514048>{interaction.user.mention} has denied your {s_loa['type']} request.",
                        color=0xff3c3c
                    )
                    await user.send(embed=success)
                    await self.bot.loas.update_by_id(s_loa)
                    role = discord.utils.get(interaction.guild.roles, id=self.loa_role)
                    await user.add_roles(role)
                except Exception as e:
                    raise Exception(e)
                    pass
                self.value = True
                await interaction.edit_original_response(view=self)
                self.stop()
                continue



class RemoveWarning(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.value = None
        self.user_id = user_id

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        self.value = True

        success = discord.Embed(
            title="<:CheckIcon:1035018951043842088> Removed Warning",
            description="<:ArrowRightW:1035023450592514048>I've successfully removed the warning from the user.",
            color=0x71c15f
        )

        await interaction.edit_original_response(embed=success, view=self)
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='No', style=discord.ButtonStyle.danger)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        self.value = False

        success = discord.Embed(
            title="<:ErrorIcon:1035000018165321808> Cancelled",
            description="<:ArrowRightW:1035023450592514048>The warning has not been removed from the user.",
            color=0xff3c3c
        )

        await interaction.edit_original_response(embed=success, view=self)
        self.stop()
class RemoveWarning(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.value = None
        self.user_id = user_id

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        self.value = True

        success = discord.Embed(
            title="<:CheckIcon:1035018951043842088> Removed BOLO",
            description="<:ArrowRightW:1035023450592514048>I've successfully removed the BOLO from the user.",
            color=0x71c15f
        )

        await interaction.edit_original_response(embed=success, view=self)
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='No', style=discord.ButtonStyle.danger)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        self.value = False

        success = discord.Embed(
            title="<:ErrorIcon:1035000018165321808> Cancelled",
            description="<:ArrowRightW:1035023450592514048>The BOLO has not been removed from the user.",
            color=0xff3c3c
        )

        await interaction.edit_original_response(embed=success, view=self)
        self.stop()

class CustomSelectMenu(discord.ui.View):
    def __init__(self, user_id, options: list):
        super().__init__()
        self.value = None
        self.user_id = user_id

        self.add_item(CustomDropdown(self.user_id, options))
