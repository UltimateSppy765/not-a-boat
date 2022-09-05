import disnake as discord
from disnake.ext import commands

activitiesjson={
    "YouTube Together": "755600276941176913",
    "Watch Together": "880218394199220334",
    "Poker Night": "755827207812677713",
    "Betrayal.io": "773336526917861400",
    "Fishington.io": "814288819477020702",
    "Chess In The Park": "832012774040141894",
    "Sketchy Artist": "879864070101172255",
    "Awkword": "879863881349087252",
    "Putts": "832012854282158180",
    "Doodle Crew": "878067389634314250",
    "Letter Tile": "879863686565621790",
    "Word Snacks": "879863976006127627",
    "Spellcast": "852509694341283871",
    "Checkers In The Park": "832013003968348200",
    "Poker Night Dev": "763133495793942528",
    "Watch Together Dev": "880218832743055411",
    "Doodle Crew Dev": "878067427668275241",
    "Word Snacks Dev": "879864010126786570",
    "Sketchy Artist Dev": "879864104980979792",
    "Decoders Dev": "891001866073296967",
    "CG2 Dev (Chess)": "832012586023256104",
    "CG3 Dev (Checkers)": "832012682520428625",
    "CG4 Dev": "832013108234289153",
    "Poker Night Staging": "763116274876022855",
    "CG2 Staging (Chess)": "832012730599735326",
    "CG3 Staging (Checkers)": "832012938398400562",
    "Poker Night QA": "801133024841957428",
    "CG2 QA (Chess)": "832012815819604009",
    "CG3 QA (Checkers)": "832012894068801636"
}

class ActivityInvite(commands.Cog):
    def __init__(self,client):
        self.client=client
        
    @commands.slash_command(name='start-activity')
    async def start_activity(self,itr,channel:discord.VoiceChannel,activity:str):
        try:
            activity=int(activity)
        except:
            await itr.response.send_message(':x: Please enter a valid application ID of the activity.',ephemeral=True)
        return await itr.response.send_message(content=f':white_check_mark: Successfully generated activity invite! (Invite is valid for a day.)\n{str(await channel.create_invite(max_age=86400,target_application=int(activity),target_type=discord.InviteTarget.embedded_application))}')
    
    @start_activity.autocomplete('activity')
    async def acstart_autocomp(self,itr,string:str):
        rjson={}
        if string=="":
            for i in list(activitiesjson.keys()):
                if len(rjson)>=25:
                    break
                else:
                    rjson[i]=activitiesjson[i]
        else:
            for i in list(activitiesjson.keys()):
                if len(rjson)>=25:
                    break
                if string.strip().lower() in i.lower():
                    rjson[i]=activitiesjson[i]
        return rjson
    
    @start_activity.error
    async def start_activity_error(self,itr,error):
        if isinstance(error,commands.CommandInvokeError):
            if isinstance(error.original,discord.HTTPException):
                return await itr.response.send_message(f':x: Failed to create an activity invite to the given channel. ```\n{error.original.text}\n```',ephemeral=True)

def setup(client):
    client.add_cog(ActivityInvite(client))
