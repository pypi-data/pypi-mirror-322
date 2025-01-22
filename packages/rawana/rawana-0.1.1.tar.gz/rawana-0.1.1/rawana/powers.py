class Powers:
    def __init__(self):
        self.powers_list = {
            "immortality": "Blessed with immortality by Lord Brahma, Rawana cannot be killed by any divine being or force.",
            "strength": "Possesses the strength of a thousand elephants, able to perform feats of unimaginable power.",
            "flight": "Ability to fly through the skies at incredible speeds, making him almost unstoppable.",
            "shape_shifting": "Can transform into any form at will, deceiving even the most powerful beings.",
            "weapons": "Mastery over celestial weapons, including the powerful Brahmastra, capable of destroying entire worlds.",
            "invulnerability": "Protected from death by nearly every weapon and source of harm, except for a few rare exceptions.",
            "wisdom": "Possesses immense wisdom and knowledge of ancient sciences, able to see through time and space.",
            "dark_magic": "Can summon and control powerful dark forces, using them to manipulate the fabric of reality.",
            "command_over_rakshasas": "Commands an army of rakshasas, supernatural beings bound by his will, to do his bidding.",
            "illusion_creation": "Able to create complex illusions, making the real world indistinguishable from his created reality.",
            "superhuman_hearing": "Has the ability to hear sounds from great distances and understand the intentions of others.",
            "regeneration": "Can rapidly heal from any injury, no matter how severe, thanks to his mastery over magical arts.",
            "telepathy": "Able to communicate mentally with others, bypassing physical limitations such as distance or language.",
            "invocation_of_vishnu": "Can invoke the power of Lord Vishnu for a limited time, gaining unimaginable strength and control over the universe.",
            "control_over_elements": "Can manipulate the natural elements — earth, water, fire, and air — with a mere thought.",
            "time_manipulation": "Able to alter the flow of time, speeding it up or slowing it down to his advantage.",
            "astral_projection": "Can leave his physical form and travel through astral planes, gaining knowledge and power from other realms.",
            "curse_of_vulnerability": "Despite his many boons, Rawana is cursed with vulnerability to being defeated by a human warrior, as granted by Lord Brahma.",
            "command_over_night": "Has dominion over the night, able to bring darkness wherever he wishes, shrouding areas in eternal night.",
            "perfect_memory": "Possesses a flawless memory, able to recall even the most minute details from his past or the world around him."
        }
    
    def get_all_powers(self):
        """Return all of Rawana's powers"""
        return self.powers_list
    
    def get_power_description(self, power_name):
        """Get description of a specific power"""
        return self.powers_list.get(power_name, "Power not found")
