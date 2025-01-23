class Stories:
    def __init__(self):
        self.story_collection = {
            "origin": """
            Rawana, the powerful demon king of Lanka, was born to sage Vishrava and his wife Kaikesi, a rakshasi (demon). 
            Vishrava was a learned and wise sage, and Kaikesi was the daughter of a demon king. This union resulted in Rawana 
            and his siblings, who were endowed with immense strength and power. Rawana's birth was marked by extraordinary signs, 
            with his destiny being shaped by divine forces.
            Rawana was a brilliant scholar, a master of the Vedas, and a highly skilled warrior, eventually ascending the throne of Lanka.
            """,
            
            "tapasya": """
            Rawana's most defining moment in his early life was his severe penance (tapasya) to Lord Brahma. 
            Rawana desired immortality and supreme power, and for this, he underwent thousands of years of meditation 
            and self-mortification. His meditation was so intense that he sacrificed his own heads ten times to please Brahma.
            Moved by Rawana's unwavering dedication, Brahma granted him boons, including near invulnerability. 
            However, Brahma's blessing came with the condition that Rawana could be defeated by a human, which would later 
            be the cause of his downfall.
            """,
            
            "battle_with_devas": """
            After receiving his boon from Brahma, Rawana's power grew exponentially. He became the terror of the Devas (gods), 
            defeating several of their best warriors. He fought many gods, including Indra, the king of the heavens, and even 
            defeated Lord Shiva in battle. His arrogance grew, and he began challenging the celestial order. 
            Rawana's reign of terror extended across the three worlds — heaven, earth, and the underworld. 
            His ambition knew no bounds, and his conflict with the gods would set the stage for a divine confrontation.
            """,
            
            "abduction_of_sita": """
            Rawana's most notorious act was the abduction of Sita, the wife of Lord Rama, an incarnation of the god Vishnu. 
            When Lord Rama, along with his brother Lakshmana, was in exile in the forest, Rawana, driven by lust and obsession, 
            kidnapped Sita. Disguising himself as a beggar, he lured Sita into his chariot and took her to his kingdom of Lanka. 
            This act of abduction, driven by his desire to possess Sita, led to a great war between Rawana and Rama. 
            It was the catalyst that eventually brought about Rawana's demise.
            """,
            
            "final_battle": """
            The final confrontation between Rawana and Rama is the central event of the *Ramayana*. 
            Rama, with the help of his loyal ally Hanuman and his army of monkeys, marched towards Lanka. 
            After an epic battle, Rama faced Rawana on the battlefield. Despite Rawana's immense powers, 
            his fate was sealed when Rama, with divine guidance from Lord Vishnu, fired an arrow that struck Rawana's heart. 
            This arrow, imbued with divine energy, killed Rawana and ended his reign of terror. 
            His death symbolized the victory of good over evil.
            """,
            
            "rebirth_of_ravana": """
            Some interpretations of the *Ramayana* and later texts like the *Mahabharata* suggest that Rawana's soul was not entirely destroyed 
            after his death. According to certain beliefs, Rawana's soul would return in different forms, still possessing his dark powers. 
            However, this is more of a symbolic representation of his essence rather than a literal rebirth. 
            It emphasizes the enduring struggle between good and evil, with Rawana's dark influence continuing to challenge the forces of righteousness.
            """,
            
            "rawana_in_ramayana": """
            Rawana, though a demon king, is portrayed as a highly complex character in the *Ramayana*. 
            Despite his many negative traits, such as arrogance, obsession, and greed, Rawana was also a great scholar, a devout worshipper of Lord Shiva, 
            and a protector of his people. His devotion to Shiva led him to obtain great powers, and his wisdom in matters of governance was widely recognized. 
            Rawana's multifaceted nature reflects the deeper themes in the *Ramayana*, where characters often embody both virtues and flaws. 
            His tragic flaw, however, was his pride and disregard for the moral order, which ultimately led to his downfall.
            """,
            
            "lessons_from_ravana": """
            Rawana's life serves as a reminder of the consequences of unchecked ambition and arrogance. 
            His deep devotion to Shiva and his pursuit of knowledge and power are admirable qualities, 
            but his inability to recognize his limitations and his ego-driven actions led him astray. 
            The *Ramayana* teaches that wisdom, humility, and righteousness are the true sources of strength, 
            and that even the mightiest of warriors can fall if they abandon these virtues.
            """
        }
    
    def get_story(self, story_name):
        """Get a specific story about Rawana"""
        return self.story_collection.get(story_name, "Story not found")
    
    def get_all_stories(self):
        """Get all available stories"""
        return list(self.story_collection.keys())
