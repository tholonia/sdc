import random

# def shiftary(a):
#     a = list(a)
#     loops = random.choice([1,2,3,4]) #^ '4' is arbitray, and assume there are at least classes of type (biology, insects, etc)
#     for j in range(loops):
#         items = a[:5] #^ 5 is half of 10, which is the the number of elements in easy class aray (of biology, insects, etc)
#         for item in items:
#             a.remove(item)
#             a.append(item)
#     return a


artists=["Thomas Kinkade,landscape art,painter","Vincent Van Gogh,cityscape,landscape art","Leonid Afremov,painter","Claude Monet,landscape art,portrait","Edward Hopper,genre painting,american realism","Norman Rockwell,realism,figurative art","William-Adolphe Bouguereau,mythological painting,pont-aven school","Albert Bierstadt,landscape art,painter","John Singer Sargent,landscape art,portrait","Pierre-Auguste Renoir,mythological painting,landscape art","Frida Kahlo,surrealism,portrait","John William Waterhouse,pre-raphaelite brotherhood,neo-pompeian","Winslow Homer,realism,marine art","Walt Disney","Thomas Moran,explorer,landscape art","Phil Koch","Paul C?zanne,landscape art,genre painting","Camille Pissarro,landscape art,the wrightsman pictures","Erin Hanson,artist","Thomas Cole,landscape art,painter","Raphael,mythological painting,allegory","Steve Henderson,designer","Pablo Picasso,sculptor,painter","Caspar David Friedrich,landscape art,german romanticism","Ansel Adams,artsy artist id,artsy","Diego Rivera,muralist,museum of modern art online collection","Steve McCurry,photographer","Bob Ross,landscape art,painter","John Atkinson Grimshaw,mythological painting,landscape art","Rob Gonsalves,magic realism,painter","Paul Gauguin,landscape art,tate artist id","James Tissot,realism,japonisme","Edouard Manet,landscape art,genre painting","Alphonse Mucha,symbolism,poster artist","Alfred Sisley,painter,still life","Fabian Perez,painter","Gustave Courbet,realism,landscape art","Zaha Hadid,architectural painting,architect","Jean-L?on G?r?me,academic art,neo-pompeian","Carl Larsson,landscape art,genre painting","Mary Cassatt,landscape art,genre painting","Sandro Botticelli,mythological painting,early renaissance","Daniel Ridgway Knight,genre painting,landscape art","Joaqu?n Sorolla,portrait,impressionism","Andy Warhol,portrait,pop art","Kehinde Wiley,painter,contemporary art","Alfred Eisenstaedt,photographer,portrait","Gustav Klimt,landscape art,religious art","Dante Gabriel Rossetti,figurative art,allegory","Tom Thomson,landscape art,painter","Edgar Degas,genre painting,impressionism","Utagawa Hiroshige,landscape art,painter","Camille Corot,realism,landscape art","Edward Steichen,photographer,pictorialism","David Hockney,digital art,graphics","Ivan Aivazovsky,mythological painting,landscape art","Josephine Wall,painter,fantasy","Peter Paul Rubens,mythological painting,landscape art","Henri Rousseau,landscape art,figure painting","Edward Burne-Jones,mythological painting,genre painting","Pixar","Alexander McQueen,designer","Anders Zorn,landscape art,marine art","Jean Auguste Dominique Ingres,romanticism,neoclassicism","Franz Xaver Winterhalter,landscape art,academic art","Katsushika Hokusai,japonisme,portrait","John Constable,realism,landscape art","Canaletto,landscape art,painter","Shepard Fairey,graffiti artist,contemporary art","Gordon Parks,film director,social realism","George Inness,landscape art,painter","Anthony van Dyck,mythological painting,allegory","Vivian Maier,street photography,photographer","Catrin Welz-Stein","Lawren Harris,landscape art,painter","Salvador Dali,landscape art,allegory","David Bowie,rock ?n? roll is here to pay,montreux jazz festival database","Agnes Cecile","Titian,mythological painting,venetian school","Martin Johnson Heade,landscape art,marine art","Scott Naismith","William Morris,arts and crafts movement,decorative arts","Berthe Morisot,portrait painting,painter","Vladimir Kush,painter","William Holman Hunt,pre-raphaelite brotherhood,portrait","Edvard Munch,landscape art,genre painting","Joseph Mallord William Turner,landscape art,marine art","Gustave Dor?,romanticism,allegory","Thomas Eakins,realism,art of painting","Ilya Repin,realism,genre painting","Amedeo Modigliani,landscape art,portrait","Johannes Vermeer,genre painting,portrait","Eyvind Earle,painter","Ivan Shishkin,realism,landscape art","Rembrandt Van Rijn,mythological painting,landscape art","Gil Elvgren,painter","Nicholas Roerich,mythological painting,landscape art","Henri Matisse,landscape art,neo-impressionism","Thomas Gainsborough,landscape art,rococo","Artgerm","Studio Ghibli","Grant Wood,landscape art,regionalism","Jeremy Mann,researcher","Mark Keathley","Maxfield Parrish,genre art,mythological painting","Andrew Wyeth,realism,landscape art","RHADS","David Lynch,magic realism,independent cinema usa","Frederic Remington,realism,landscape art","Jan Van Eyck,northern renaissance,genre painting","Mikko Lagerstedt","Banksy,contemporary art,graffiti","Michael Cheval,actor","Anna Razumovskaya,lady-in-waiting","Jean-Fran?ois Millet,genre painting,landscape art","Thomas W Schaller","Charlie Bowater","El Greco,mythological painting,landscape art","Paolo Roversi,photographer","Carne Griffiths","Man Ray,abstract art,assemblage","August Sander,photographer","Andrew Macara,painter","Evelyn De Morgan,pre-raphaelite brotherhood,painter","William Blake,romanticism,allegory","Sally Mann,landscape art,contemporary art","Oleg Oprisco","Yuumei,visual artist","Helmut Newton,photographer","Henry Ossawa Tanner,realism,landscape art","Asher Brown Durand,landscape art,painter","teamLab","August Macke,landscape art,painter","Armand Guillaumin,impressionism,painter","Terry Redlin,artist","Antoine Blanchard,painter,school of paris","Anna Ancher,impressionism,painter","Ohara Koson,printmaker,nihonga","Walter Langley,painter","Yayoi Kusama,abstract art,feminist art","Stan Lee,publisher,comics","Chuck Close,contemporary art,portrait","Albert Edelfelt,realism,painter","Mark Seliger,photographer","Eugene Delacroix,landscape art,romanticism","John Lavery,painter,portrait","Theo van Rysselberghe,neo-impressionism,painter","Marc Chagall,landscape art,religious art","Rolf Armstrong,painter","Brent Heighton","A.J.Casson","Egon Schiele,landscape art,allegory","Maximilien Luce,painter,pointillism","Georges Seurat,landscape art,genre painting","George Frederic Watts,symbolism,academic art","Arthur Hughes,pre-raphaelite brotherhood,painter","Anton Mauve,hague school,painter","Lucian Freud,school of london,landscape art","Jessie Willcox Smith,illustrator","Leonardo Da Vinci,high renaissance,painter","Edward John Poynter,history painting,painter","Brooke Shaden,photographer","J.M.W. Turner,landscape art,marine art","Wassily Kandinsky,abstract art,graphics","Wes Anderson,film director","Jean-Honor? Fragonard,landscape art,painter","Amanda Clark,researcher","Tom Roberts,artist,heidelberg school","Antonello da Messina,portrait painting,early renaissance","Makoto Shinkai,animated film,film director","Hayao Miyazaki,film director","Slim Aarons,photographer","Alfred Stevens,realism,painter","Albert Lynch,genre painting,painter","Andre Kohn","Daniel Garber,landscape art,painter","Jacek Yerka,painter,surrealism","Beatrix Potter,fairy tale,writer","Rene Magritte,cityscape,landscape art","Georgia O?Keeffe,abstract art,floral painting","Isaac Levitan,realism,painter","Frank Lloyd Wright,architect","Gustave Moreau,mythological painting,sculptor","Ford Madox Brown,pre-raphaelite brotherhood,painter","Ai Weiwei,conceptual art,installation art","Tim Burton,film director","Alfred Cheney Johnston,photographer","Duy Huynh","Michael Parkes,researcher","Tintoretto,painter","Archibald Thorburn,painter","Audrey Kawasaki,painter","George Lucas,film producer,speculative fiction film","Arthur Streeton,landscape art,painter","Albrecht Durer,mythological painting,landscape art","Andrea Kowch,painter","Dorina Costras","Alex Ross,comics artist","Hasui Kawase,shin-hanga,landscape art","Lucas Cranach the Elder,mythological painting,german renaissance","Briton Rivi?re,academic art,painter","Antonio Mora,researcher","Mandy Disher","Henri-Edmond Cross,painter,neo-impressionism","Auguste Toulmouche,genre painting,painter","Hubert Robert,pre-romanticism,landscape art","Syd Mead,designer,neo-futurism","Carl Spitzweg,post-romanticism,painter","Alyssa Monks,painter,portrait","Edward Lear,landscape art,writer","Ralph McQuarrie,artist","Sailor Moon","Simon Stalenhag,artist","Edward Robert Hughes,painter","Jules Bastien-Lepage,painter,potato","Richard S. Johnson,impressionism,painter","Rockwell Kent,landscape art,painter","Sparth","Arnold B?cklin,landscape art,portrait","Lovis Corinth,mythological painting,landscape art","Arnold Bocklin,landscape art,portrait","Robert Hagan,naval officer","Gregory Crewdson,photographer","Thomas Benjamin Kennington,genre painting,painter","Abbott Handerson Thayer,landscape art,painter","Gilbert Stuart,portrait,painter","Louis Comfort Tiffany,artist,art nouveau","Raphael Lacoste,art director","Jean Marc Nattier,history painting,painter","Janek Sedlar,photographer","Sherree Valentine Daines,visual artist","Alexander Jansson,illustrator","James Turrell,land art,light and space","Alex Grey,figurative art,performance artist","Henri De Toulouse Lautrec,genre painting,animal painting","Anton Pieck,painter","Ramon Casas,impressionism,painter","Andrew Atroshenko","Andy Kehoe","Andreas Achenbach,landscape art,painter","H.P. Lovecraft","Eric Zener,painter","Kunisada,utagawa school,ukiyo-e artist","Jimmy Lawlor,association football player","Quentin Tarantino,action film,actor","Marianne North,landscape art,floral painting","Vivienne Westwood,designer,punk counterculture","Tom Bagshaw","Jeremy Lipking,painter","John Martin,romanticism,landscape art","Cindy Sherman,artsy artist id,feminist art","Scott Listfield","Alexandre Cabanel,genre painting,academic art","Arthur Rackham,fairy painting,painter","Arthur Hacker,painter,portrait","Henri Fantin Latour,realism,mythological painting","Mark Ryden,painter","Peter Holme III","Ted Nasmith,artist","Bill Gekas,photographer","Paul Strand,photographer","Anne Stokes,artist,illustrator","David Teniers the Younger,mythological painting,landscape art","Alan Lee,painter","Ed Freeman,helicopter pilot","Andrey Remnev,iconographer","Alasdair McLellan,photographer","Botero,figurative art,allegory","Vittorio Matteo Corcos,portrait painting,genre painting","Ed Mell,painter","Worthington Whittredge,painter","Jakub R??alski,illustrator","Alex Gross,painter","Edward Weston,photographer","Ilya Kuvshinov,artist","Francisco De Goya,mythological painting,romanticism","Balthus,landscape art,surrealism","J.C. Leyendecker","Nathan Wirth","Albert Goodwin,painter","Ferdinand Hodler,symbolism,painter","Charles Spencelayh,genre painting,painter","Louise Dahl-Wolfe,photographer","Amy Judd,researcher","Kitagawa Utamaro,ukiyo-e artist,ukiyo-e","Igor Zenin","Carlo Crivelli,painter,gothic art","Edmund Leighton,genre painting,pre-raphaelite brotherhood","Bjarke Ingels,architect","Diego Vel?zquez,mythological painting,landscape art","Bernardo Bellotto,cityscape,landscape art","John Singleton Copley,portrait painting,artist","Horace Vernet,landscape art,romanticism","Hiroshi Yoshida,association football player","Walter Crane,symbolism,painter","Anka Zhuravleva","Robert Mcginnis,painter","John Wilhelm","Anna Dittmann","Bo Bartlett,realism,painter","Michal Karcz","Mort Kunstler,painter","Adrianus Eversen,painter","Brad Kunkle","Bella Kotak","Paul Delvaux,painter","Victo Ngai,illustrator","Abbott Fuller Graves,realism,painter","Patrice Murciano","Alexandre Calame,landscape art,painter","Bob Byerley","Cicely Mary Barker,painter","Kadir Nelson,graphic designer","Kengo Kuma,architect","Brothers Grimm","Jovana Rikalo","Malcolm Liepke","Bert Stern,photographer,portrait","Alice Neel,cityscape,landscape art","Moebius,western film,comics","Alex Colville,painter","Andreas Franke,volleyball player","Gjon Mili,photographer","Arthur Wardle,painter","Alan Bean,military officer","Ernst Ludwig Kirchner,landscape art,genre painting","Kevin Sloan,association football player","Miho Hirano","Russ Mills","Boris Kustodiev,genre art,painter","Andrea Mantegna,mythological painting,allegory","Hsiao-Ron Cheng","Carl Holsoe,painter","Jeff Goldblum,western,television actor","Tadao Ando,boxer","Tibor Nagy,researcher","Charles-Francois Daubigny,painter,landscape art","Jacob Lawrence,genre painting,figure painting","Andre Derain,landscape art,fauvism","Bert Hardy,photographer","?lisabeth Vig?e Le Brun,rococo,portrait","Jeremy Geddes,painter","Peter Wileman,visual artist","Ary Scheffer,history painting,painter","Coles Phillips,artist","Francis Bacon,figurative art,surrealism","Olafur Eliasson,abstract art,installation artwork","Eric Wallis,researcher","Alexander Millar,librarian","Andre Kertesz,photographer","Peter Mohrbacher","Jean-Michel Basquiat,figurative art,biography.com","Akseli Gallen-Kallela,symbolism,romanticism","George Tooker,painter","Stevan Dohanos,painter","Diane Arbus,portrait photography,photographer","Sofonisba Anguissola,genre painting,portrait","James Abbott McNeill Whistler,landscape art,marine art","Igor Morski","Ray Caesar,painter","Pierre Bonnard,landscape art,tate artist id","Helene Schjerfbeck,painter,naturalism","Gerda Wegener,painter,portrait","Paolo Veronese,venetian school,allegory","Pieter Bruegel The Elder,landscape art,northern renaissance","Anne-Louis Girodet,mythological painting,romanticism","John Duncan,neurologist","Paul Corfield","Gaston Bussi?re,symbolism,painter","Flora Borsi,artist","Howard Pyle,writer,brandywine school","Eduardo Kobra,street artist","Edwin Henry Landseer,romanticism,landscape art","Odd Nerdrum,painter","Alberto Giacometti,abstract art,landscape art","Edmund Dulac,painter,orientalism","Takashi Murakami,figurative art,sculptor","John Currin,painter,contemporary art","Robert McCall,ice dancer","Artemisia Gentileschi,mythological painting,portrait","Guo Pei,fashion designer","Bartolome Esteban Murillo,genre painting,baroque painting","Raja Ravi Varma,painter,portrait","Adrian Smith,heavy metal guitarist,heavy metal","Honor? Daumier,caricature,figure","Remedios Varo,landscape art,surrealism","Ernst Haeckel,biologist","Bess Hamiti","Marie Spartali Stillman,landscape art,pre-raphaelite brotherhood","Albert Marquet,painter,fauvism","Jeanloup Sieff,photographer","Ismail Inceoglu","Berndnaut Smilde,sculptor","Donato Giancola,science fiction,painter","Guillermo del Toro,psychological thriller,horror film","Bill Brandt,symbolism,photographer","Santiago Calatrava,high-tech architecture,sculptor","Marco Mazzoni,artist","Cyril Rolando","Craig Davison","Richard Burlet","Victor Nizovtsev,painter","Roger Dean,illustrator","Norman Foster,architect,high-tech architecture","Joseph Lorusso","Aron Wiesenfeld,comics artist","Zinaida Serebriakova","Marc Simonetti,illustrator","James Paick","Sam Spratt","Andreas Rocha","James Jean,painter","Michael Whelan,illustration,fantastic realism","M.C. Escher,abstract art,cityscape","Frank Frazetta,painter,fantasy art","Serge Marshennikov,painter","Louis Icart,painter","Alberto Vargas,painter","Frank Gehry,architect,postmodern architecture","Frederick McCubbin,landscape art,painter","John Howe,illustrator","Shaun Tan,writer","Dora Maar,photographer,surrealism","Giorgio De Chirico,abstract art,cityscape","Georges de La Tour,classicism,genre painting","Anthony Thieme,painter","Alex Andreev,painter","Thomas Saliot","Louis Janmot,painter","Laurie Lipton,artist","Hyacinthe Rigaud,portrait,baroque painting","Alson Skinner Clark,landscape art,painter","Mikhail Nesterov,landscape art,religious art","Konstantin Korovin,painter,still life","Otto Dix,mythological painting,landscape art","Iain Faulkner,painter","Alfred Munnings,painter","Casey Weldon,american football player","Karol Bak,painter","Antony Gormley,figurative art,contemporary art","Rebeca Saray","Antoni Gaudi,catalan modernism,architect","Henry Asencio,painter,portrait","Carrie Mae Weems,social-artistic project,installation art","Brent Cotton","Kim Keever,artist","Thomas Allom,architect","Gabriele M?nter,cityscape,portrait","Johann Wolfgang von Goethe,theatre manager,sturm und drang","Piet Mondrian,abstract art,landscape art","John James Audubon,landscape art,animal painting","Jessica Rossier","Adolph Menzel,realism,painter","Thomas Blackshear,painter","Paul Klee,abstract art,surrealism","Kazimir Malevich,abstract art,figurative art","Ian McQue","Bruce Pennington,painter","Michael Carson,researcher","Eugene von Guerard,painter","Michelangelo Merisi Da Caravaggio,genre painting,painter","Jean Fouquet,renaissance,painter","Sou Fujimoto,architect","Naoto Hattori","Carl Gustav Carus,landscape art,botanist","Simeon Solomon,pre-raphaelite brotherhood,history painting","Tyler Shields,photographer","Max Ernst,abstract art,dada","Annibale Carracci,genre painting,painter","Kelly Vivanco","Frederic Church,landscape art,painter","Nick Knight,photographer","Peter Gric,painter,surrealism","Tristan Eaton,muralist","Alex Timmermans","Kate Greenaway,painter","Arthur Lismer,painter","Th?odore G?ricault,romanticism,painter","Pieter de Hooch,landscape art,genre painting","John Salminen,landscape art,painter","Stephan Martiniere,artist","Max Dupain,photographer","Coby Whitmore,illustrator","Edwin Austin Abbey,art of painting,painter","Filippino Lippi,italian renaissance,painter","Anish Kapoor,abstract art,contemporary art","Max Weber,jurist","Ben Aronson,abstract expressionism,painter","Irma Stern,modern art,genre painting","John Berkey,painter","Beeple,visual artist","JC Leyendecker","Vhils,muralist","Paul Henry,painter","Dan Witz,painter","Dora Carrington,painter,bloomsbury group","Peter Max,graphics,batik","Francis Coates Jones,painter","Fernand Toussaint,painter","Albert Joseph Moore,symbolism,painter","Atey Ghailan","Jean Nouvel,architect","David Burdeny,photographer","Brian M. Viveros","Sacha Goldberger,photographer","Olivier Valsecchi","Henry Moore,abstract art,figurative art","Zack Snyder,film director","ROA","Jeremiah Ketner","Louise Bourgeois,abstract art,assemblage","Jean-Antoine Watteau,f?te galante,painter","Albert Watson,photographer","Art Frahm,painter","David Ligare,painter","Brian Kesinger,animator","James C Christensen,researcher","Phil Noto,comics artist","Marsden Hartley,abstract art,dada","Franz Marc,abstract art,landscape art","Herbert List,photographer","Aykut Aydogdu","Alexej von Jawlensky,cityscape,landscape art","John La Farge,painter,portrait","Tom Lovell,painter","tokyogenso","Dr. Seuss,fairy tale,writer","NC Wyeth","Leonora Carrington,mythological painting,painter","Will Barnet,painter","Elizabeth Gadd,researcher","Boris Grigoriev,painter,russian avant-garde","Jacob van Ruisdael,landscape art,painter","Alberto Seveso","Patrick Brown,biochemist","Sean Yoro","Noah Bradley,artist","Loish,illustrator","Ivan Bilibin,illustrator,book illustration","Roy Lichtenstein,pop art,still life","Jeffrey T. Larson","Umberto Boccioni,landscape art,figurative art","Viktor Vasnetsov,symbolism,history painting","Bordalo II,painter","Juan Gris,abstract art,figurative art","Ryan McGinley,photographer,contemporary art","Boris Vallejo,science fiction art,painter","William Etty,painter","Anton Raphael Mengs,painter,portrait","Pierre Puvis de Chavannes,symbolism,history painting","John French Sloan,landscape art,ashcan school","Augustus John,enciclopedia universal ilustrada europeo-americana,volume","Arthur Tress,photographer","James Ensor,cityscape,portrait","Mike Worrall,visual artist","Konstantin Yuon,painter,landscape art","Andreas Gursky,artist","John Bauer,painter","Alessio Albi","Greg Hildebrandt,illustrator","James Gilleard","Paul Ranson,symbolism,painter","Pawel Kuczynski,caricature,painter","Alessandro Allori,allegory,religious art","Alfred Parsons,botanical illustrator","John Frederick Kensett,painter,landscape art","Alex Prager,photographer","Aaron Jasinski","Joel Meyerowitz,photographer","Liam Wong,researcher","Raymond Leech,botanist","Brian Froud,painter","Reginald Marsh,painter,urban art","Gediminas Pranckevicius","Alex Katz,landscape art,figurative art","Charles Camoin,painter,portrait","Emmanuelle Moureaux,architect","Jeff Koons,tate artist id,conceptual art","Chris Moore,illustrator","Alfred Augustus Glendening,landscape art,painter","Mead Schaeffer,painter","Filip Hodas","Georg Jensen,designer,art nouveau","Howard Chandler Christy,landscape art,artist","Carel Willink,magic realism,painter","Alejandro Burdisio","Edwin Deakin,landscape art,painter","Dan Mumford","Sandy Skoglund,photographer","William Hogarth,realism,genre painting","Maria Kreyn","Dean Cornwell,realism,painter","Aubrey Beardsley,symbolism,aestheticism","Bastien Lecouffe-Deharme,photographer","Jean Metzinger,figurative art,landscape art","William Wegman,photographer","Clara Peeters,painter,still life","Paul Gustav Fischer,cityscape,realism","Jeff Legg","Ross Tran,visual artist","Koson Ohara,printmaker,nihonga","Sandra Chevrier,contemporary artist","Abraham Pether,painter","Jamie Hawkesworth,photographer","Odilon Redon,landscape art,allegory","Iwan Baan,photographer","Giuseppe de Nittis,painter","Craig Mullins,illustrator","Emilia Wilk","Skottie Young,illustrator","Francis Picabia,abstract art,dada","?mile Bernard,cityscape,mythological painting","Anne Packard","Alex Alemany,painter","Alan Kenny","Gerhard Richter,abstract art,cityscape","Eug?ne Grasset,symbolism,type designer","Bernard Buffet,landscape art,painter","Anatoly Metlan","Sir James Guthrie,painter,portrait","William Henry Hunt,painter,portrait","Andre De Dienes,photographer","Kay Nielsen,figurative art,sculptor","Alain Laboile,photographer","Alex Maleev,comics artist","Adrian Donoghue","Damien Hirst,assemblage,vanitas","Aaron Douglas,actor","Ben Goossens,photographer","Mike Campau","Thomas Dodd,biographer","Frank Holl,painter,portrait","Lyonel Feininger,painter,expressionism","Adriaen van Ostade,genre painting,painter","Chesley Bonestell,illustrator","Carlos Schwabe,symbolism,painter","Chen Zhen,visual artist","Ando Fuchs","Douglas Smith,singer","Hikari Shimoda","Luis Royo,painter,fantasy","John Harris,publisher","Chris Leib","Frederick Lord Leighton,mythological painting,allegory","Rebecca Louise Law,installation artist","Max Beckmann,mythological painting,landscape art","Tomasz Alen Kopera,painter","Yanjun Cheng","Raymond Swanland","Clive Madgwick,painter","Hendrik Kerstens,photographer","Rick Guidice","Jason Edmiston","Jim Lee,comics artist","Matthias Jung,researcher","Henry Moret,impressionism,painter","Anne Bachelier,artist","Mary Blair,illustrator","Tove Jansson,novel,painter","Peter Zumthor,architect","Ruth Bernhard,photographer","Chiharu Shiota,installation art,installation artist","Raphaelle Peale,still life,painter","Hans Baldung,german renaissance,portrait","Alois Arnegger,painter","James Gurney,illustrator","Peter Sculthorpe,composer,opera","Elizabeth Shippen Green,illustrator","Everett Raymond Kinstler,painter,portrait","Edward Atkinson Hornel,painter","George Luks,painter,retrieved","Hendrick Avercamp,painter","Harriet Backer,art of painting,graphics","Ryohei Hase,baseball player","Joe Webb,american football player","Brian Despain,artist","Christophe Vacher,background artist","Anton Corbijn,film director","George Grosz,dada,new objectivity","Charles Dana Gibson,illustrator,portrait","Mark Brooks,researcher","Armand Point,symbolism,painter","Jasmine Becket-Griffith,artist","Ambrosius Benson,northern renaissance,painter","Giuseppe Arcimboldo,allegory,religious art","Wadim Kashin","Kent Monkman,artist","Susan Seddon Boulet","Pieter Aertsen,renaissance,history painting","Beth Conklin","Brian Mashburn,film actor","Uemura Shoen,painter,nihonga","Alfred Guillou,q62090257,painter","Evgeni Gordiets,painter","David Inshaw,pop art,painter","Pieter Claesz,painter,still life","Alvin Langdon Coburn,photographer","Jean Delville,symbolism,painter","Augustus Edwin Mulready,genre painting,painter","Wim Wenders,new german cinema,film director","Alex Garant","Cha?m Soutine,portrait painting,landscape art","Rebecca Guay,painter","Martine Johanna","Hope Gangloff,painter,contemporary art","Eero Saarinen,modernism,architect","Alan Moore,comics,comics writer","Cuno Amiet,painter,pont-aven school","David Choe,painter","Brett Weston,photographer","Julie Bell,painter","James Montgomery Flagg,artist","Neil Welliver,painter","Henry Fuseli,romanticism,fairy painting","Michael Sowa,researcher","Emil Nolde,landscape art,watercolor","Robert S. Duncanson,landscape art,portrait","Jackson Pollock,abstract art,abstract expressionism","Jean Giraud,western film,comics","Andy Fairhurst","Alan Schaller","Esao Andrews,painter","Daniel Buren,painter","Anton Semenov,researcher","Fairfield Porter,painter","George Stubbs,landscape art,romanticism","Craola","Hilma AF Klint,abstract art,landscape art","Akos Major,judge","Mark Lovett,basketball player","Christopher Balaskas","Mati Klarwein,painter,surrealism","David A. Hardy,illustrator","Peter Howson,genre painting,contemporary art","Barkley L. Hendricks,painter,contemporary art","It? Jakuch?,painter","William S. Burroughs,writer,science fiction","Fernand Khnopff,symbolism,painter","Alexei Harlamoff,painter,portrait","Dan Flavin,installation art,minimalism","Grace Cossington Smith,painter","Andrew Ferez","Robert Irwin,light and space,painter","Bruno Walpoth,sculptor","Ernst Haas,photographer","Peter Kemp,swimmer","Jaume Plensa,digital art,figurative art","Kathryn Morris Trotter","Arthur Sarnoff,illustrator","Simon Birch,buddy film,drama film","Dale Chihuly,abstract art,contemporary art","Karen Wallis","Antonio Donghi,magic realism,landscape art","Marianne von Werefkin,symbolism,painter","Ryan Hewett","Alice Pasquini,artist","Joan Mir?,abstract art,graphics","Helene Knoop,painter","Mike Mignola,comics artist","Larry Elmore,comics artist","Artem Chebokha","Giotto Di Bondone,mythological painting,allegory","Richard Misrach,photographer","Martin Deschambault","Alessandro Gottardo,comics artist","Agostino Arrivabene,painter","Zdzis?aw Beksi?ski,painter","Gareth Pugh,fashion designer","Kelly Mckernan","Adi Granov,comics artist","Debbie Criswell","Artur Bordalo,painter","Amanda Sage,painter","Marek Okon","Alfred Henry Maurer,modernism,painter","Silvestro Lega,realism,painter","Sakai Ho?itsu,painter,rimpa school","Elsa Beskow,children?s literature,writer","Michelangelo Buonarroti,sculptor,high renaissance","Josh Keyes,american football player","Ben Shahn,photographer,social realism","Antonio Canova,mythological painting,figurative art","Mikhail Vrubel,symbolism,painter","Beauford Delaney,painter,harlem renaissance","Hugh Ferriss,architect","Tamara Lempicka,portrait,painter","Yves Klein,abstract art,figurative art","Andy Goldsworthy,land art,photographer","Android Jones","Harry Clarke,arts and crafts movement,painter","Liu Ye,actor","Frank Miller,film director","Michael Hutter,actor","Roberto Ferri,painter","Kay Sage,abstract art,landscape art","Ernie Barnes,painter","Andr? Lhote,painter,portrait","Auguste Herbin,painter,oxford dictionary of modern and contemporary art","Hiroshi Sugimoto,figurative art,contemporary art","Jon Whitcomb,military officer","Chris Foss,painter","Marina Abramovi?,conceptual art,performance artist","Mark Rothko,abstract art,painter","Albert Gleizes,landscape art,section d?or","Joseph Stella,landscape art,religious art","Joey Chou","Jane Newland","Catherine Hyde","Bertil Nilsson,association football player","Paul Lehr,painter","Takato Yamamoto,painter","Goro Fujita,go professional","Robert Vonnoh,painter,portrait","Billy Childish,garage punk,poet","Yasutomo Oka","James Thomas Watts,painter","Martin Ansin","Zeen Chin","Ken Kelly,speculative fiction,painter","Josan Gonzalez","Brian K. Vaughan,screenwriter","Kobayashi Kiyochika,mangaka,ukiyo-e","Hugh Kretschmer","Ben Quilty,painter,portrait","Fenghua Zhong","Bettina Rheims,photographer","Aleksey Savrasov,realism,landscape art","Alice Bailly,painter","Adam Hughes,comics artist","Bernardo Strozzi,painter","Franklin Booth,artist","Greg Girard,photographer","Anna Bocek","Natalia Goncharova,futurism,painter","Gifford Beal,painter","Paul Chadeisson,concept artist","Adolf Hir?my-Hirschl,painter","Lori Earley,painter","F Scott Hess","Dorothea Tanning,figurative art,painter","Jasper Johns,abstract art,figure","Saul Steinberg,comics artist","Grayson Perry,figurative art,artist","Ferdinand Knab,painter","Mickalene Thomas,painter,contemporary art","Constantin Brancusi,abstract art,tinerimea artistic?","Tokujin Yoshioka,designer","Bill Medcalf","Mark Arian","Afarin Sajedi,artist","Tomer Hanuka,cartoonist","Jason Chan,researcher","Cassius Marcellus Coolidge,painter","Antonio Mancini,painter,portrait","Martiros Saryan,graphics,illustration","Lee Madgwick","Tim Doyle,screenwriter","Les Edwards,painter","Fabio Hurtado,painter","Tim Hildebrandt,painter","Sonia Delaunay,abstract art,landscape art","Charles Angrand,incoherents,portrait","Loretta Lux,photographer","Kawanabe Ky?sai,painter","Keith Haring,figurative art,contemporary art","Amandine Van Ray","Lisa Keene,painter","Alphonse Osbert,symbolism,painter","Storm Thorgerson,photographer","Annie Soudain","Bill Jacklin,painter","Bill Ward,drummer,hard rock","Kilian Eng,dramaturge","Samuel Melton Fisher,painter","Haddon Sundblom,painter","Rodney Matthews,artist","George French Angas,explorer","Bruce Munro,lighting designer","Alastair Magnaldo","Ellen Jewett","William Stout,painter","Julie Blackmon,photographer","Alena Aenami","C. R. W. Nevinson,ambulance driver,landscape art","Lois van Baarle,illustrator","Apollinary Vasnetsov,landscape art,history painting","Samuel Earp","Saturno Butto,painter","Richard Dadd,landscape art,marine art","Anja Percival,visual artist","Michal Lisowski","Tara McPherson,illustrator","Paula Modersohn-Becker,painter,expressionism","Klaus Wittmann,translator","Annie Swynnerton,painter","Daniel Merriam,geologist","Ida Rentoul Outhwaite,illustrator","Robert Farkas,researcher","Nicolas Mignard,mythological painting,painter","Anselm Kiefer,abstract art,landscape art","Ron Mueck,figurative art,artist","Robert Rauschenberg,assemblage,museum of modern art online collection","George Ault,painter,precisionism","Robby Cavanaugh","Hieronymus Bosch,northern renaissance,genre painting","Hale Woodruff,painter","Andrei Markin,politician","David Bomberg,painter,vorticism","Anni Albers,designer","Grandma Moses,na?ve art,folk art","Victor Vasarely,abstract art,kinetic art","Robert Williams,hip hop music,trap music","Diego Dayer","Bob Eggleton,artist","Reylia Slaby","Eric Fischl,painter","Bill Carman","Arthur Boyd,landscape art,figurative art","Austin Osman Spare,symbolism,artist","Faith Ringgold,artsy artist id,painter","Alan Parry,sports commentator","Oskar Kokoschka,landscape art,painter","Scarlett Hooft Graafland,photographer","Mary Anning,paleontologist","Anna and Elena Balbusso","Sydney Prior Hall,painter,portrait","Nikolai Ge,russian symbolism,history painting","Aristarkh Lentulov,painter,post-impressionism","Bayard Wu","Jesper Ejsing","Richard Doyle,fairy painting,retrieved","Brett Whiteley,painter","Arthur Dove,painter","Gwen John,painter,portrait","Richard Lindner,pop art,new figuration","Kaws","Benedick Bana","Andreas Levers","Zanele Muholi,photographer","Maurice Sendak,graphic designer","Bridget Riley,abstract art,artsy artist id","Bill Viola,new media art,video art","Norman Ackroyd,painter","John Anster Fitzgerald,fairy painting,painter","Brothers Hildebrandt","Alexandr Averin","Charles E. Burchfield,painter","Richard Diebenkorn,abstract art,abstract expressionism","Albert Dubois-Pillet,painter,pointillism","Thomas Rowlandson,romanticism,caricaturist","Frank Stella,abstract expressionism,shaped canvas","Robert Antoine Pinchon,painter,landscape art","Gertrude Abercrombie,landscape art,surrealism","Hendrick Goltzius,history painting,painter","Ludwig Mies van der Rohe,modernism,architect","Yves Tanguy,abstract art,painter","Stephen Shore,photographer","Conrad Roset,illustrator","William Eggleston,photographer","Candido Portinari,modern art,painter","Jamie Baldridge,artist","Salomon van Ruysdael,landscape art,painter","Edward Gorey,writer","Jack Kirby,superhero comics,science fiction","Eddie Mendoza","Arnold Schoenberg,serialism,20th-century classical music","Margaret Macdonald Mackintosh,painter,art nouveau","Tatsuro Kiuchi","Os Gemeos","Charles Schulz,cartoonist","Mike Mayhew,painter,stuckism","Charles Vess,artist,retrieved","Dustin Nguyen,actor","Piet Hein Eek,designer","Pieter Jansz Saenredam,painter","Alvaro Siza,architect","Ruan Jia","Sue Bryce","Virgil Finlay,illustrator","Nicolas Delort,visual artist","Atelier Olschinsky","Tracey Emin,installation art,sales representative","Zhichao Cai","Isaac Cordal,sculptor","Shohei Otomo,artist","Tyler Edlin,artist","Erich Heckel,painter,expressionism","Dave Dorman,illustrator","Tom Whalen,politician","Jean Bourdichon,engraver","Jim Davis,cartoonist","Fang Lijun,painter","Ivan Albright,portrait,figure","Barbara Hepworth,abstract art,catalan modernism","Hans Baluschek,painter,expressionism","Milo Manara,comics,comics artist","Milton Glaser,designer","Tim White,historical novel,fantasy","Yasuo Kuniyoshi,still life,catalan modernism","Alexandre Benois,painter","Yinka Shonibare,contemporary art,photographer","Alex Russell Flint","Emmanuel Shiu","Jamie McKelvie,cartoonist","Angela Barrett,researcher","Simone Martini,sienese school,painter","Joanna Kustra","Travis Louie","Raymond Briggs,writer","Jos? Clemente Orozco,genre painting,mural","Bojan Jevtic,researcher","Sean Scully,painter","J?zef Mehoffer,fribourg cathedral,portrait","Quint Buchholz,author","Shaddy Safadi,artist","Peter Elson,illustrator","Hayv Kahraman,painter","Jed Henry","John Atherton,priest","Adam Elsheimer,painter","Bijou Karman","Ray Donley,artist","Quentin Blake,children?s writer","Louis Wain,artist","Frank Auerbach,painter,contemporary art","Krenz Cushart","Masamune Shirow,animator","L?szl? Moholy-Nagy,abstract art,painter","Roger de La Fresnaye,painter,cubism","Claude Cahun,artist,self-portrait","Kenne Gregoire,painter","Louis Rhead,poster artist","Aliza Razell","Satoshi Kon,animator","Abigail Larson,cross-country skier","Aaron Siskind,photographer","Brian Stelfreeze,cover artist","Stanley Donwood,artist","Antanas Sutkus,photographer","Gustaf Tenggren,illustrator","Jean Jullien,illustrator","Richard Eurich,painter","Paul Wonner,abstract expressionism,painter","Rich Davies","Paulus Potter,landscape art,genre painting","Wolf Kahn,painter","Lynd Ward,illustrator,wordless novel","Justin Gerard,researcher","Willem de Kooning,abstract art,abstract expressionism","Alvar Aalto,architect","Hajime Sorayama,artist,erotic art","Jim Burns,painter","Jenny Saville,painter,nude","Donald Judd,abstract art,artist","Nan Goldin,contemporary art,photographer","David Finch,comics artist","Jeff Simpson,tennis player","Victoria Crowe,painter","Alexey Kurbatov,sport cyclist","Edward Julius Detmold,artist","Francesca Woodman,artsy artist id,self-portrait","Rob Liefeld,editor","Albert Koetsier","Zhang Kechun,photographer","Darren Bacon","Randolph Caldecott,painter","Lady Pink,painter","Charles Schridde","Bill Sienkiewicz,comics artist","Giacomo Balla,futurism,painter","Andreas Vesalius,anatomist","Ettore Tito,painter,portrait","Naomi Okubo","Octavio Ocampo,artist","Ub Iwerks,film director","Charles Blackman,artist","Anton Domenico Gabbiani,baroque,painter","Cory Loftis,animator","Robert Crumb,cartoonist","Chris Ware,illustrator","Annick Bouvattier","Ambrosius Bosschaert,still life,floral painting","Daniela Uhlig","John Philip Falter,painter","Thomas Struth,photographer","Ingrid Baars,photographer","Adam Martinakis,artist","Jean Arp,abstract art,dada","Nobuyoshi Araki,figurative art,contemporary art","Roger Ballen,photographer","K?the Kollwitz,figurative art,printmaker","Santiago Caruso","Jacob Hashimoto,artist","Laurie Greasley","Guy Billout,caricaturist","Saul Tepper,illustrator","Will Eisner,comics artist","Charles Le Brun,classicism,portrait","John Wayne Gacy,clown","Viviane Sassen,contemporary art,photographer","Abram Efimovich Arkhipov,realism,painter","Max Pechstein,painter,expressionism","Jordan Grimmer","Mike Deodato,comics artist","Greg Rutkowski","Bhupen Khakhar,painter","David Palumbo,poster artist","Jeff Lemire,comics writer","Clemens Ascher","?mile Gall?,?cole de nancy,art nouveau","Cedric Peyravernay","Brooke DiDonato","Warren Ellis,journalist","Darwyn Cooke,comics artist","Jerry Pinkney,writer","Carl Barks,actor","Victor Brauner,surrealism,symbolism","Anne Mccaffrey,speculative fiction,writer","Anton Otto Fischer,marine art,artist","Johannes Voss,researcher","Robert Maguire,painter","Adrian Ghenie,modernism,painter","Mab Graves","Meryl McMaster,painter","Ralph Horsley,artist","Aleksi Briclot,comics artist","Laurel Burch,painter","Joe Bowler","Lorenz Hideyoshi","Anne Dewailly,visual artist","Gabriel Dawe,artist","Magnus Enckell,symbolism,painter","Raymond Duchamp-Villon,sculptor,cubism","Tony DiTerlizzi,fantastic fiction,juvenile sciencefiction","Gerhard Munthe,painter","Qian Xuan,painter","Katsuhiro Otomo,manga,screenwriter","Masaaki Sasamoto,painter","Daryl Mandryk","Jean-Baptiste Monge,painter","David Burliuk,russian futurism,poet","Rufino Tamayo,modernism,painter","Joel Sternfeld,photographer","Antonio J. Manzanedo","Craig Wylie,painter","Adonna Khare,artist","Chris Turnham","Anne Sudworth,painter","Alec Soth,photographer","Emory Douglas,artist","Aristide Maillol,symbolism,les nabis","Adam Paquette","Brad Rigney","Maximilian Pirner,painter","William Zorach,sculptor,cubism","Richard Hamilton,pop art,painter","Phil Jimenez,penciller","George Cruikshank,caricaturist,painter","Bill Brauer","Pascal Blanche,comics artist","Angus McKie,illustrator","Leonetto Cappiello,poster artist,portrait","Anato Finnstark","Juergen Teller,photographer","Jeff Wall,landscape art,contemporary art","Jeff Easley,painter","Costa Dvorezky","Don Maitz,illustrator","Franz Sedlacek,magic realism,painter","Kelly Sue Deconnick,comics writer","Alexandre-E?variste Fragonard,troubadour style,sculptor","Leiji Matsumoto,film director","Amir Zand","Albert Pinkham Ryder,landscape art,romanticism","Kris Kuksi,sculptor","Keith Parkinson,painter","Keith Negley","Ashley Wood,comics artist","Geof Darrow,comics artist","Mike Winkelmann (Beeple)","Larry Sultan,photographer","Gerald Brom,illustrator","Bruce Timm,comics artist","Patrick Dougherty,researcher","Arthur Stanley Wilkinson,artist","Takeshi Obata,mangaka","Glen Orbik,comics artist","Pipilotti Rist,installation art,feminism","Qing Han,researcher","Anton Fadeev","Chris Van Allsburg,writer","Ettore Sottsass,architect","Claire Hummel","Tsutomu Nihei,mangaka","Jorge Jacinto,researcher","Zhelong Xu,researcher","Josef Albers,abstract art,painter","Daniel Clowes,cartoonist","Steve Argyle,artist","William Kentridge,film director","Kim Jung Gi,comics artist","Arshile Gorky,abstract art,abstract expressionism","Joe Jusko,artist","Dave McKean,comics,photographer","Andrew Robinson,television actor","Tomi Ungerer,children?s literature,erotic literature","Kitty Lange Kielland,landscape art,painter","David Driskell,artist","Brandon Woelfel","Mark Briscoe,professional wrestler","Diane Dillon,illustrator","Bryan Hitch,comics artist","Dean Ellis,illustrator","Sydney Edmunds","Johannes Itten,painter,expressionism","Kelly Freas,illustrator","Ed Binkley","Adrian Paul Allinson,painter","Yiannis Moralis,painter","Axel T?rneman,painter","Dmitry Kustanovich,landscape art,painter","Honor C. Appleton,painter","Artus Scheiner,painter","Joseph Ducreux,painter,portrait","Todd McFarlane,cartoonist","Dao Le Trong","Doug Chiang,film director","William Gropper,lithographer","Stuart Immonen,comics artist","Roberto Parada,actor","Alex Howitt","Michael Heizer,abstract art,land art","Lisa Frank,businessperson","Junji Ito,writer,horror comics","Ernst Fuchs,architect","Jim Mahfood,comics writer","Grace Popp","Adrian Tomine,illustrator","Tom Hammick,visual artist","Charles Gwathmey,architect","Marie Guillemine Benoist,genre painting,neoclassicism","Thornton Oakley,painter","Robert Motherwell,abstract art,painter","Iryna Yermolova","Brian Bolland,comics artist","Joe Madureira,comics artist","Arthur Adams,zoologist","Ren? Lalique,goldsmith,art deco","Jon Klassen,writer","Peter Doig,painter","Chad Knight,actor","Marcin Jakubowski,researcher","Bill Henson,photographer","Joe Fenton,artist","Alexandre Jacovleff,neoclassicism,painter","Blek Le Rat,police officer","Hou China","Taiy? Matsumoto,mangaka","Dorothy Lathrop,writer","Giovanni Battista Gaulli,painter,fresco painting","Sidney Nolan,retrieved,painter","Kieron Gillen,journalist","Josh Kao","Klaus Burgle,graphic designer","Jamie Hewlett,comics artist","Elenore Abbott,painter,art nouveau","Yoshitaka Amano,character designer","theCHAMBA","Ayami Kojima,engineer","Jan van Kessel the Elder,still life,floral painting","Todd Schorr,painter","Barbara Kruger,artsy artist id,conceptual art","Hiroshi Nagai,researcher","Apollonia Saintclair,illustrator,erotic art","Jake Parker,illustrator","Chris Saunders,visual artist","Yoji Shinkawa,illustrator","Akihiko Yoshida,video game developer","Anne Brigman,artsy artist id,photographer","Karl Schmidt-Rottluff,impressionism,sculptor","Alfred Kubin,symbolism,writer","Winsor McCay,cartoonist","Ian Miller,archaeologist","Viktoria Gavrilenko","Dain Yoon","Victor Adame Minguez","Peter De Seve,artist","Frank Tinsley,illustrator","Yue Minjun,painter","Jamini Roy,kalighat painting,folk art","Albert Tucker,retrieved,painter","Alex Horley,comics artist","Yohann Schepacz","Al Feldstein,journalist","Olivier Bonhomme,researcher","Joseph Cornell,film director","Glenn Fabry,painter","Ben Templesmith,screenwriter","Andr? Masson,painter,surrealism","Ed Brubaker,comics writer","Becky Cloonan,comics artist","Barnett Newman,abstract art,color field","W. Heath Robinson,comics artist","Marc Davis,screenwriter","Richard Deacon,actor","Brian Sum,researcher","OSGEMEOS","Jerry Siegel,comics writer","Wendy Froud,dollmaker","Chris Mars,artist,alternative rock","Nicola Samori,painter","Camille Walala","Maria Sibylla Merian,lepidopterist","Barthel Bruyn the Elder,portrait painting,german renaissance","Milton Caniff,comics artist","Akira Toriyama,mangaka,fantasy","Joe De Mers","Conor Harrington,painter","Philip Guston,abstract art,abstract expressionism","Elaine de Kooning,abstract art,painter","Seb Mckinnon,artist","Kuang Hong","Barry Windsor Smith,comics artist","Paul Barson","Georges Rouault,symbolism,curator","Ruxing Gao","Ed Emshwiller,video artist","Agnes Martin,abstract art,abstract expressionism","Rafa? Olbi?ski,painter","Greg Simkins,painter,lowbrow","Bernie Wrightson,comics artist","Lee Krasner,abstract art,painter","Piotr Jab?o?ski,amateur wrestler","Alejandro Jodorowsky,surrealism,writer","Jeannette Guichard-Bunel,painter","Jack Davis,cartoonist","Bridget Bate Tichenor,painter,surrealism","John Bratby,painter","Steven Belledin","Helen Frankenthaler,abstract art,abstract expressionism","Neil Boyle,researcher","Hannah Hoch,dada,photomontage","Yuri Ivanovich Pimenov,scenography,painter","Ralph Steadman,caricaturist","Tony Moore,penciller","Clyde Caldwell,illustrator,fantasy","Bruno Catalano,sculptor","M?ret Oppenheim,dada,assemblage","August Friedrich Schenck,animal painting,landscape art","Karl Blossfeldt,photographer,new objectivity","Mikhail Larionov,rayonism,neo-impressionism","Jean-Paul Riopelle,les automatistes,painter","Ed Roth,artist","Siya Oum","Roz Chast,cartoonist","Vincent Di Fate,artist","Johfra Bosschart,magic realism,painter","Giovanni Battista Piranesi,neoclassicism,landscape art","Patrick Woodroffe,artist","Butcher Billy","Lucy Madox Brown,genre painting,pre-raphaelite brotherhood","Alex Schomburg,painter","Alex Figini","Genndy Tartakovsky,film director","Jean Dubuffet,abstract art,outsider art","Bruce Nauman,installation art,postminimalism","Albert Bloch,painter,expressionism","Julie Mehretu,abstract art,visual artist","Frank Xavier Leyendecker,illustrator","Nikolina Petolas","Gwenda Morgan,printmaker","David Shrigley,painter,contemporary art","Alexander Archipenko,abstract art,sculptor","Alexander Kanoldt,painter,expressionism","Wangechi Mutu,contemporary art,figure","JennyBird Alcantara","Mat Collishaw,video recording,contemporary art","Desmond Morris,retrieved,surrealism","Laurent Grasso,artist","David Wiesner,writer","Nicolas de Stael,abstract art,still life","Ogawa Kazumasa,photographer","Tyler West,television presenter","Steve Dillon,comics artist","John Stezaker,painter,contemporary art","Ron Walotsky,video game artist","Don Bluth,film director","Scott Brundage","Alexandre Antigna,realism,painter","Pamela Colman Smith,illustrator","Heinrich Kley,caricaturist","Wayne Barlowe,novelist","Stuart Davis,american modernism,painter","Jillian Tamaki,comics artist","Al Williamson,comics artist","Cagnaccio Di San Pietro,painter","Sarah Lucas,abject art,installation art","Brice Marden,painter,minimalism","Brenda Zlamany,painter","Jason A. Engle","Rafael Albuquerque,painter","Affandi,painter,expressionism","Robert Chew,researcher","Osamu Tezuka,film director","Terry Oakes","Liang Mark","Alex Toth,comics artist","Marius Borgeaud,painter","John Blanche,illustrator","Ann Stookey","E. H. Shepard,artist","Chip Zdarsky,comics artist","James Gillray,caricaturist","Jeffrey Catherine Jones,artist","Naoki Urasawa,manga,mangaka","Edouard Riou,painter,orientalist painting","Giovanni Battista Venanzi,painter","Nagel Patrick","Vincent Tanguay","Daniele Afferni","Barthel Bruyn the Younger,portrait painting,painter","Chris Claremont,writer","Asaf Hanuka,caricaturist","Shinji Aramaki,film director","Clara Miller Burd,glass artist","Etienne Hebinger","Haroon Mirza,visual artist,contemporary art","Marjane Satrapi,screenwriter","John Cassaday,comics artist","Arturo Souto,painter","Colin Geller","Gloria Stoll Karn,printmaker,portrait","Robert Stivers,lawyer","Ernest Crichlow,painter,social realism","Jon McCoy,basketball player","Art Spiegelman,comics artist","Farel Dalrymple,cartoonist","Shintaro Kago,mangaka","Art Fitzpatrick,animator","Milton Avery,painter","Constant Permeke,painter,expressionism","August von Pettenkofen,landscape art,painter","Guido Borelli Da Caluso,painter","Gaetano Pesce,architect","Peter Milligan,screenwriter","Margaret Mee,botanical illustrator","Bo Chen,researcher","Kate Beaton,cartoonist","Albert Eckhout,painter","Richard Corben,graphic designer","Jack Butler Yeats,painter","Mao Hamaguchi","Hethe Srodawa","Hanna-Barbera","Leon Kossoff,painter,expressionism","Hein Gorny,photographer","Chris Ofili,figurative art,painter","Clarence Holbrook Carter,painter","Naoko Takeuchi,illustrator","Amy Earles","Mikalojus Konstantinas Ciurlionis,western classical music,art nouveau","Joao Ruas,visual artist","Algernon Blackwood,writer","Issac Levitan","Miriam Schapiro,abstract art,artsy artist id","Kaethe Butcher","Ferdinand Van Kessel,painter,flemish baroque painting","Eddie Campbell,comics artist","Bill Traylor,outsider art,painter","Enki Bilal,comics artist","Howard Finster,folk art,painter","Jun Kaneko,artist","Matti Suuronen,architect","Albert Robida,journalist,science fiction","Charles Liu,astrophysicist","Willem van Haecht,baroque painting,painter","Alan Davis,comics artist","David Spriggs,sculptor","Sebastian Errazuriz,artist","Kentaro Miura,mangaka","Eileen Agar,painter,surrealism","Hal Foster,comics artist","Emil Alzamora","Eleanor Vere Boyle,pre-raphaelite brotherhood,painter","Abraham Mintchine,painter","Jan Brett,writer","Shin Jeongho,politician","Simon Bisley,comics artist","Dariusz Zawadzki,association football player","Marc Samson,music critic","Chantal Joffe,painter","Julia Contacessi","Matt Fraction,comics writer","Ethan Van Sciver,comics artist","Emily Kame Kngwarreye,painter","Anto Carte,painter","Sam Bosma,illustrator","Kevin Gnutzmans","Amiet Cuno","Albrecht Anker,portrait painting,impressionism","Harold McCauley","Steve Lieber,penciller","Jim Woodring,cartoonist","Allen Williams,actor","Gustave Buchet,painter","Tomokazu Matsuyama,contemporary artist","Eiichiro Oda,mangaka","Patrick Heron,painter,contemporary art","Barbara Takenaga,painter","Noriyoshi Ohrai,illustrator","L. Birge Harrison,painter","Till Freitag","John Kenn Mortensen,voice actor","Pascale Campion","Posuka Demizu,illustrator","Basil Gogos,illustrator","George Herriman,cartoonist","Ossip Zadkine,abstract art,abstraction","David McClellan","Francisco Mart?n,researcher","Cliff Chiang,comics artist","Roy Gjertson","Gustave Van de Woestijne,symbolism,painter","Lorena Alvarez G?mez","Alessandro Barbucci,comics artist","Heinrich Lefler,painter","Go Nagai,mangaka","Dave Gibbons,comics artist","Arthur Radebaugh,illustrator","Ching Yeh,researcher","Christian Dimitrov,racing driver","Alayna Lemmer","Alison Bechdel,cartoonist","William Steig,writer","Jacques Nathan-Garamond,painter","Andrzej Sykut","Guido Crepax,erotic comic,comics artist","Larry Poons,painter","Matt Groening,animator","Alfredo Jaar,visual artist","Ronald Balfour,historian","Tan Zhi Hui,pop music,singer","Philippe Druillet,graphic designer","Benoit B. Mandelbrot,mathematician","Stephen Oakley,classical philologist","Oskar Fischinger,painter","Ellen Gallagher,abstract art,figurative art","Faith 47","Henry Raleigh,artist","Emma Geary,artist","Victor Medina,association football player","Sheilah Beckett,illustrator","Aaron Horkey,graphic designer","Judy Chicago,artsy artist id,feminist art","Adolph Gottlieb,abstract art,painter","David Aja,comics artist","Kati Horna,photographer","Nick Sharratt,writer","Lyubov Popova,singer","?tienne-Louis Boull?e,schoolteacher","Alma Thomas,abstract art,abstract expressionism","Maxwell Boas","Arkhyp Kuindzhi","Andre Norton,science fiction,fantasy","Bart Sears,comics artist","Thomas Visscher","Alfred Heber Hutty,painter","Jean-Louis Prevost,neurologist","Ben Nicholson,abstract art,painter","Barclay Shaw,artist","Hans Bellmer,painter,surrealism","Ayan Nag","Brian Oldham","Stuart Haygarth","Walter Percy Day,painter","Wojciech Ostrycharz","Ken Fairclough","Walt Kelly,comics artist","Albert Servaes,painter,expressionism","Ravi Zupa","John Whitcomb","Jeff Kinney,author","Maria Pascual Alberich,drawer","Stephen Gammell,illustrator","Roberto Matta,abstract art,painter","Muxxi","Walter Kim","Carmen Saldana,researcher","Boris Groh,visual artist","Aquirax Uno,painter","Giovanni Battista Bracelli,painter","Alberto Burri,assemblage,art of painting","Steve Ditko,comics artist","Filippo Balbi,painter","Jimmy Ernst,abstract expressionism,painter","Alex Petruk","Wim Crouwel,type designer","Teophilus Tetteh","Patrick Caulfield,pop art,painter","Inio Asano,mangaka","Leticia Gillett","Liubov Sergeevna Popova,abstract art,cityscape","Richard Scarry,children?s literature,writer","Bruce Coville,writer","Richard McGuire,cartoonist,montreux jazz festival database","Pixar Concept Artists","Alexis Gritchenko,painter","W.W. Denslow,artist","Jan Pietersz Saenredam","Andre-Charles Boulle,sculptor","Alberto Sughi,painter","Rudolf Freund,mathematician","Michael Deforge,comics artist","Cory Arcangel,digital art,musician","Aminollah Rezaei,poet","Aggi Erguna","Sangyeob Park","Ni Chuanjing","Hirohiko Araki,mangaka","Matt Bors,comics artist","Bill Durgin","Shawn Coss","Barry McGee,painter","J. J. Grandville,symbolism,caricaturist","James Stokoe,comics artist","Saner Edgar","Etel Adnan,painter,hurufiyya movement","Angela Sung","Luisa Russo,penciller","Allison Bechdel","Samuel and Joseph Newsom","Anne Truitt,sculptor,minimalism","Matthias Gr?newald,religious art,figure","Martin Kippenberger,abstract art,sculptor","Ken Sugimori,illustrator","Christian Grajewski","Yasushi Nirasawa,illustrator","Kuno Veeber,sculptor,constructivism","Herve Groussin","Romero Britto,neo-pop,pop art","John Perceval,painter","Alberto Biasi,painter","Noelle Stevenson,comics artist","Alexander Fedosav","Bakemono Zukushi","Ul Di Rico","Ted Wallace,politician","Rayner Alencar","Alexander Milne Calder,sculptor","Abdel Hadi Al Gazzar,painter","Jacques Le Moyne,cartographer","Howard Hodgkin,painter,contemporary art","Squeak Carnwath,painter","Ed Benedict,animator","Alfred Kelsner,illustrator","Jeffrey Smith art","Teresa Ramos,researcher","Ewald R?bsamen,zoologist","Asger Jorn,cobra,situationist international","Al Capp,cartoonist","Anne Rothenstein,painter","Jessica Woulfe","Mordecai Ardon,artist","Bernard Aubertin,textile artist","Atay Ghailan","Bill Watterson,cartoonist","Abed Abdi,ironworker","Hendrick Cornelisz Vroom,painter,marine art","Shusei Nagaoko","Anita Malfatti,avant-garde,painter","Agostino Tassi,landscape art,painter","H. R. (Hans Ruedi) Giger","Robert William Hume","Sanford Kossin","Julien Delval,illustrator","Norman Bluhm,abstract expressionism,painter","Heinz Edelmann,designer","Istvan Banyai,animator","Hans Arnold,illustrator","Stanislav Poltavsky","Klaus Janson,comics artist","Eliott Lilly","Charline von Heyl,abstract art,painter","Albert Kotin,abstract expressionism,painter","Alex Hirsch,animator","Derek Boshier,contemporary art,sculptor","Yang Jialun","Jan Luyken,engraver","Amadou Opa Bathily","Tari Ma?rk Da?vid","Earl Norem,painter","Shotaro Ishinomori,mangaka","Helio Oiticica,abstract art,tropic?lia","Susan Luo,researcher","Frits Van den Berghe,painter,expressionism","Charles Addams,illustrator","Wilfredo Lam,figurative art,painter","Saul Bass,graphic designer","Margaret Brundage,painter","Alice Rahon,painter,surrealism","Louis Glackens,caricaturist","Peter Bagge,writer","David B. Mattingly,painter","Barbara Stauffacher Solomon,painter","Lynda Barry,cartoonist","Bojan Koturanovic","NHK Animation","Alexander Bogen,art of painting,painter","Otto Marseus van Schrieck,baroque,painter","Gordon Browne,painter","John Totleben,comics artist","Kasia Nowowiejska,illustrator","Sven Nordqvist,writer","Jhonen Vasquez,comics artist","Briana Mora","Raina Telgemeier,cartoonist","Philippe Parreno,visual artist","Olga Skomorokhova","Jef Wu","Ai Yazawa,mangaka","Henriette Grindat,photographer","Patricia Polacco,writer","Anja Millen","Rumiko Takahashi,mangaka","Berend Strik,painter","Andrew Whem","Christopher Jin Baron","Brandon Mably","Aron Demetz,sculptor","Augustus Jansson,artist,art deco","Lee Quinones,graffiti artist","Robert M Cunningham","Ephraim Moses Lilien,photographer","Robert Neubecker","Nick Silva","Jaya Suberg","Victor Moscoso,cartoonist","Peter Andrew Jones,illustrator","Chris Cunningham,film director","Stan And Jan Berenstain,writer","Tex Avery,film director","Joachim Brohm,photographer","Robert Childress,illustrator","Yoshiyuki Tomino,mecha,film director","Guerrilla Girls,photographer,feminist art","John Hoyland,painter,contemporary art","Giovanni da Udina","Rebecca Sugar,screenwriter","Elliot Lilly","Agnes Lawrence Pelton,landscape art,painter","Yaacov Agam,abstract art,artist","Ashley Willerton","Emil Ferris,comics artist","Toumas Korpi","Ollie Hoff","Jack Gaughan,illustrator","Clovis Trouille,restorer","Toei Animations","?Friedensreich Regentag "," Dunkelbunt Hundertwasser?","Toshiharu Mizutani","Am?d?e Guillemin,journalist","Jerzy Duda-Gracz,painter","Yayi Morales","Arthur Garfield Dove,painter","Amedee Ozenfant,purism,painter","Ryan Stegman,comics artist","Martin John Heade","RETNA (Marquis Lewis)","Incarcerated Jerkfaces","Vito Acconci,installation art,architect","Rene Laloux,animator","Wolfgang Tillmans,abstract art,contemporary art","Kurzgesagt","Adriaen van Outrecht","Bruno Munari,futurism,artist","Stanis?aw Szukalski,painter","Julian Calle,politician","Lesley Vance,painter","Sara Wollfalk","Herv? Guibert,journalist","Fernando Herenu","Antonio Roybal,painter","Raffaello Sanizo","Death Burger,slasher film,comedy horror","Karel Appel,abstract expressionism,cobra","Allie Brosh,comics artist","Kapwani Kiwanga,artist","George Dionysus Ehret","Warwick Globe","Igor Wolski","Alpo Jaakola,painter","Rodr?guez ARS","Sam Kieth,comics artist","Paul Laffoley,artist","Gary Larson,cartoonist","Arik Brauer,poet","Nathan Coley,artist,contemporary art","Antoine Verney-Carron","Benedetto Caliari,painter","Luca Boni,screenwriter","M.W. Kaluta","Georg Karl Pfahler,sculptor","Albert Benois,painter","Ben Wooten","Matias Hannecke","Marcus Selmer,photographer","Joan Tuset,painter","Lynda Benglis,abstract art,artsy artist id","Juliana Huxtable,digital art,visual artist","Jane Graverol,painter","Anthony Gerace","Alberto Magnelli,concrete art,painter","Ben Hatke,comics artist","Andre?i Arinouchkine,penciller","Terada Katsuya","Tomma Abts,painter","Amy Sillman,painter","Chris Uminga","Auguste Mambour,poster artist","Phil Foglio,comics artist","Russell Ayto,writer","Galan Pang","Kazuo Koike,comics,screenwriter","Maginel Wright Enright Barney,writer","Dick Bickenbach","Karel Thole,painter","Aries Moross,graphic designer","Margaux Valonia","Gianluca Foli,illustrator","Julius Horsthuis,artist","Nele Zirnite,etcher","Marat Latypov,researcher","Valerie Hegarty,conceptual art,installation art"]

pre = [
    # "pen and ink portrait, Aubrey Beardsley",
    # "pen and ink portrait by Aubrey Beardsley",
    "Generate a scientifically accurate, detailed, and colorful image of a ",
    "Generate a scientifically accurate, detailed, and colorful image of a ",
    # f"black and white pen and ink drawing",
    # f"polaroid photograph",
    # f"black and white photograph",
    # f"brownie camera photograph"
]

background = [
    "blackness",
    "dark black",
]

places=[
    "forest",
    "jungle",
    "swamp",
    # "desert",
    # "mountain",
    # "lake",
    "valley",
    # "city",
    # "town",
    # "road",
    "outerspace",
    "outer space",
    "river",
    # "war",
    # "slum",
    # "car"
]

style=["realistic","fantasy","beautiful","chaotic","peaceful","dangerous","complex","simple"]

adj =["amazed", "aggravated", "anxious", "attractive", "awful", "awestruck",
"bold", "chilly", "bashful", "brave", "dejected", "cautious", "bubbly",
"dirty", "composed", "cheerful", "dreadful", "easygoing", "comfortable",
"heavy", "horrified", "delightful", "irritated", "intelligent", "excited",
"pessimistic", "numb", "festive", "tearful", "puzzled", "free", "tense",
"quizzical", "jolly", "terrible", "ravenous", "optimistic", "tired",
"reluctant", "proud", "ugly", "settled", "wonderful", "weak", "shy"]

# adj = ["colorful", "pretty"]

verbs = ["arising", "beating", "betting", "biting", "bleeding", "blowing",
"building", "catching", "creeping", "cuting", "drawing", "dreaming",
"drinking", "driving", "eating", "falling", "feeding", "fighting",
"fleeing", "flying", "freezing", "hanging", "hiding", "hitting", "holding",
"kneeling", "leading", "meeting", "reading", "riding", "ringing", "rising",
"running", "sewing", "shaking", "shining", "shooting", "singing", "sinking",
"siting", "sleeping", "sliding", "speaking", "spliting", "standing",
"stinging", "striking", "sweeping", "swimming", "teaching", "tearing",
"throwing", "weaving", "weeping", "writing"]

# verbs = ["above", "below"]

animals=[ "ground hog",  "prairie dog",  "mare",  "ram",  "ape",  "grizzly bear", 
    "chipmunk",  "chameleon",  "donkey",  "wildcat",  "reindeer",  "pony", 
    "aardvark",  "camel",  "elk",  "parakeet",  "canary",  "impala",  "turtle", 
    "mountain goat",  "jaguar",  "iguana",  "hyena",  "cheetah",  "bighorn", 
    "basilisk",  "llama",  "chimpanzee",  "toad",  "alligator",  "bald eagle", 
    "weasel",  "rooster",  "colt",  "wolverine",  "warthog",  "panda",  "musk-ox", 
    "fox",  "mustang",  "chinchilla",  "lion",  "snowy owl",  "rhinoceros", 
    "silver fox",  "otter",  "antelope",  "guinea pig",  "puma",  "polar bear", 
    "wolf",  "camel",  "squirrel",  "parrot",  "dingo",  "mule",  "fish",  "whale", 
    "gazelle",  "panther",  "starfish",  "dog",  "pig",  "walrus",  "duckbill platypus",
    "deer",  "giraffe",  "mongoose",  "newt",  "raccoon",  "anteater",
    "kitten",  "kangaroo",  "wombat",  "moose",  "lamb",  "dung beetle", 
    "peccary",  "seal",  "lovebird",  "opossum",  "gopher",  "orangutan", 
    "beaver",  "buffalo",  "armadillo",  "hare",  "blue crab",  "meerkat",  "mynah bird",
    "porcupine",  "lynx",  "bull",  "horse",  "leopard",  "gila monster",
    "bison",  "tiger",  "baboon",  "rat",  "chicken",  "snake",  "civet",  "ewe", 
    "koala",  "doe",  "ibex",  "stallion",  "skunk",  "fawn",  "tapir",  "muskrat", 
    "ferret",  "frog",  "gnu",  "jackal",  "porpoise",  "yak",  "eagle owl", 
    "bunny",  "octopus",  "elephant",  "woodchuck",  "zebra",  "lizard", 
    "marmoset",  "musk deer",  "mandrill",  "badger",  "crocodile",  "mink", 
    "ox",  "cat",  "shrew",  "salamander",  "bear",  "hamster",  "coyote", 
    "alpaca",  "puppy",  "sloth",  "rabbit",  "goat",  "hedgehog",  "burro", 
    "mole",  "ocelot",  "boar",  "mouse",  "sheep",  "finch",  "dormouse",  "crow", 
    "hog",  "cougar",  "monkey",  "lemur",  "cow",  "hippopotamus",  "marten", 
    "capybara",  "steer",  "ermine",  "gorilla",  "bat"]

birds=[ "Pigeon", "Ibis bird", "Spoonbill bird", "Hornbill bird", "Macaw bird",
    "Mynah bird", "Eagle", "Grackle bird", "Owl", "Hawk", "Finch",
    "Egret", "Gull", "Kingfisher", "Buzzard", "Crow", "Raven", "Condor",
    "Pelican", "Starling bird", "Heron bird", "Tanager bird", "Cockatoo bird",
    "Kookaburra bird", "Vulture", "Blackbird", "Catbird", "Argus bird",
    "Parrot", "Toucan", "Canary", "Flamingo", "Dove", "Duck", "Egret", "Curassow bird",
    "Sparrow", "Falcon", "Tern bird", "Thrush bird",
    "Robin", "Cowbird", "Roadrunner", "Bluebird", "Bird-of-Paradise",
    "Cuckoo bird", "Peacock-pheasant", "Go-away-bird", "Partridge",
    "Hornbill bird", "Penguin", "Kestrel bird"
]

clothes=[ "Scarf", "Cargos", "Poncho", "Blouse", "Dress", "Pajamas", "Tie",
    "Suit", "Gown", "Jeans", "Tights", "Fleece", "Polo Shirt", "Swimwear",
    "Thong", "Corset", "Boxers", "Coat", "Knickers", "Sunglasses", "Hoody",
    "Gloves", "Top", "Skirt", "Slippers", "Bikini", "Sandals", "Socks",
    "Shirt", "Briefs", "Belt", "Sarong", "Shawl", "Kilt", "Tankini", "Bow Tie",
    "Cufflinks", "Sweatshirt", "Cardigan", "T-Shirt", "Hat", "Robe",
    "Stockings", "Blazer", "Shoes", "Tracksuit", "Jogging Suit",
    "Nightgown", "Shorts", "Lingerie", "Jacket", "Dinner Jacket",
    "Waistcoat", "Swimming Shorts", "Cummerbund", "Boots", "Overalls",
    "Underwear", "Camisole", "Bra", "Cravat"
]

fish=[ "triggerfish", "boxfish", "butterflyfish", "stonefish", "clownfish",
    "trout fish", "batfish", "paddlefish", "basselets fish", "oarfish",
    "sailfish", "starfish", "wolffish", "albacore fish", "mackerel fish",
    "flounder fish", "needlefish", "barracuda fish", "goatfish",
    "lizardfish", "pinfish", "blobfish", "pollock fish", "tuna fish",
    "hogfish", "salmon fish", "butterfish", "croaker fish", "gnomefish",
    "pigfish", "mackerel fish", "dolphin fish", "grouper fish", "swordfish",
    "stingrays", "parrotfish", "catfish", "skipjack tuna", "smelt fish",
    "searobin fish", "seahorse", "cardinalfish", "pufferfish", "snapperfish",
    "halibut fish", "bluefish", "puffers fish", "unicornfish",
    "damselfish", "hawkfish", "flatfish", "tarpon fish", "cobia fish", "cod fish", "stingray", "grouper fish", "haddock fish", "marlin fish",
    "rabbitfish", "hammerhead fish", "spadefish" ] 
    
flowers=[ "Red Rose flower", "White Orchid flower", "Yellow Chrysanthemum flower", "Purple Oleander flower", "Narcissus flower",
    "Geranium flower", "Lobelia flower", "Lavender flower", "Anemone flower", "Crocus flower", "Marigold flower", "Hyacinth flower",
    "Wisteria flower", "Impatien flower", "Hollyhock flower", "Lilac flower", "Peony flower", "Lupine flower", "Tulip flower", "Pansy flower",
    "Yarrow flower", "Salvia flower", "Dahlia flower", "Camellia flower", "Bougainvillea flower", "Foxglove flower", "Gladiolus flower",
    "Poppy flower", "Primrose flower", "Hydrangea flower", "Rhododendron flower", "Delphinium flower", "Honeysuckle flower"
]

trees=[ "pine tree", "oak tree", "birch tree", "maple tree"
]

instruments=[ "Steel Pan", "Wooden Flute", "Guitar", "Clarinet", "Trumpet",
    "Whistle", "Ukulele", "Cowbell", "Piccolo", "Acoustic Guitar", "French Horn", "Bongos", "Slide Whistle", "Bass Guitar", "Oboe", "Fiddle",
    "Steel Drums", "Bagpipes", "Violin", "Triangle", "Xylophone", "Kazoo",
    "Maracas", "Organ", "Shakers", "Zither", "Ocarina", "Harmonica",
    "Drums", "Saxophone", "Symbols", "Recorder", "Tambourine", "Spoons",
    "Turntables", "Voice", "Vibraphone", "Trombone", "Harp", "Bells", "Snare Drum", "Vocals", "Crystal Glasses", "Tuba", "Flute", "Viola",
    "Keyboard", "Bamboo Flute", "Accordion", "Piano", "Banjo"
]

snakes=[ "Viper snake", "Rattlesnake", "Cobra snake", "asp snake",
    "Black-Mamba snake", "King-Snake", "Pitviper snake", "Adder snake",
    "Boa-Constrictor snake", "Milk-Snake",
]

things=[ "boom box", "deodorant", "shoes", "sun glasses", "playing card",
    "twezzers", "bookmark", "sofa", "computer", "wallet", "headphones",
    "stop sign", "teddies", "shirt", "button", "bread", "watch",
    "thermometer", "television", "perfume", "greeting card", "bag", "socks",
    "door", "toothpaste", "vase", "drill press", "hair brush", "pen",
    "knife", "needle", "tire swing", "tomato", "fork", "bracelet", "credit card", "tissue box", "desk", "clamp", "screw", "mp3 player",
    "sandpaper", "air freshener", "candy wrapper", "soy sauce packet", "outlet",
    "conditioner", "balloon", "food", "scotch tape", "paper", "bananas",
    "shampoo", "buckle", "rubber band", "lamp shade", "glass", "lace",
    "twister", "helmet", "toe ring", "monitor", "model car", "milk",
    "pillow", "stockings", "leg warmers", "drawer", "flag", "rubber duck",
    "box", "toothbrush", "white out", "clothes", "soap", "eye liner", "mop",
    "sticky note", "checkbook", "cookie jar", "cinder block", "camera",
    "tooth picks", "chapter book", "puddle", "brocolli", "speakers", "bow",
    "glasses", "candle", "seat belt", "sidewalk", "plate", "rug", "pool stick", "glow stick", "chair", "shawl", "cell phone", "bottle",
    "hair tie", "photo album", "newspaper", "fake flowers", "paint brush",
    "sponge", "carrots", "table", "tv", "lip gloss", "rusty nail", "lamp",
    "blanket", "spring", "slipper", "thread", "lotion", "bowl", "sketch pad", "cup", "sandal", "packing peanuts", "plastic fork", "keyboard",
    "hanger", "doll", "keys", "USB drive", "pencil", "beef", "floor",
    "eraser", "clay pot", "purse", "CD", "cat", "radio", "nail file",
    "coasters", "nail clippers", "house", "grid paper", "water bottle",
    "bottle cap", "window", "thermostat", "soda can", "apple", "face wash",
    "phone", "cork", "towel", "chalk", "ring", "key chain", "shovel",
    "flowers", "book", "controller", "pants", "bed", "ice cube tray",
    "remote", "sharpie", "street lights", "canvas", "mouse pad", "toilet",
    "wagon", "washing machine", "charger", "shoe lace", "spoon", "picture frame", "money", "video games", "ipod", "blouse", "mirror", "zipper",
    "car", "couch", "truck", "chocolate", "sailboat", "magnet", "tree",
    "clock", "piano", "fridge"
]

insects=[ "beetle", "ant", "ladybug", "bee", "wasp", "spider", "butterfly",
    "moth", "firefly", "dragonfly", "butterfly", "scorpion", "locust", "ant"
]

biology = [ "hydrogen atom", "molecule", "influenze virus", "HIV virus",
    "ebola virus", "adenovirus", "rabies virus", "bacteriophage",
    "papillomavirus", "rotavirus", "hepititus C virus", "herpes virus"

    "DNA", 
    "A-DNA", 
    "B-DNA", 
    "Z-DNA", 

    "bacteria", 
    "cocci bacteria", 
    "bacilli bacteria", 
    "spirochetes bacteria", 

    "protozoa", 
    "giardia protozoa", 
    "plasmodium protozoa", 
    "amoeba protozoa", 
    "trypanosoma protozoa", 

    "fungus", 
    "teeth fungus", 
    "cup fungus", 
    "polypore fungus", 
    "puffball fungus", 
    "spores", 
    "mushrooms", 
    "mycelium", 
]

test = [ "cat", "dog", "rabbit", "elephant", "parrot", "fish", "tucan",
    "kangaroo", "tiger", "polar bear", "panther", "ferret",
]

ordered1 = [
    "hydrogen atom", 
    "molecule", 
    "DNA cell", 
    "protazoa", 
    "human cell", 
    "spores", 
    "ferns", 
    "plants", 
    "swamp", 
    "jungle with sunlight shing through the leaves", 
    "sun", 
    "solar system", 
    "universe"
]
dna = [
    "DNA", 
    "double helix", 
    "RNA", 
    "genetics", 
    "DNA", 
    "double helix", 
    "RNA", 
    "genetics", 
    "DNA", 
    "double helix", 
    "RNA", 
    "genetics", 
    "DNA", 
    "double helix", 
    "RNA", 
    "genetics", 
]
cells = [
    "human cell", 
    "virus"
    "spores", 
    "embryo", 
    "germ cell", 
    "cancer cell", 
    "plant cell", 
    "DNA cell",
    "bacteria cell", 
    "protazoa", 
    "hydrogen atom", 
    "mycelium cell", 
]
models = [
#^ center stable

    # "z4000/z4000_0.safetensors",
    "526mixV145_v145.safetensors",
    "DucHaiten-Journey_v5.6.7.2.3.safetensors",
    "526sCuspOfSerenity_v1.safetensors",  # more detail,  complex but not messy,  hydrogen atom = woman
    "colorFusionXEris_12.safetensors",  # clean,  smooth,  good colors,  bad design
    "deliberate_v2.safetensors",
    "Protogen_V2.2.ckpt",  # default SD model

    # "526mixV145_v145.safetensors [9d9156a477]",
    # # "z4000/z4000_0.safetensors [d87aac35a2]",
    # "DucHaiten-Journey_v5.6.7.2.3.safetensors [d193ccfee5]",
    # "526sCuspOfSerenity_v1.safetensors [debc7b907a]",    # more detail,  complex but not messy,  hydrogen atom = woman
    # "colorFusionXEris_12.safetensors [0eb1c40a61]",      # clean,  smooth,  good colors,  bad design
    # # "photographyAnd_10.safetensors [05532cb3ce]",        # like protogen,  basic
    # "deliberate_v2.safetensors [9aba26abdf]",
    # # "realisticVisionV20_v20.safetensors [c0d1994c73]",   # more gritty
    # "Protogen_V2.2.ckpt [bb725eaf2e]",                   # default SD model
    # # "sd-v1-4.ckpt [fe4efff1e1]",                         # pan-and-iink-ish,  grainy,  hydrogen atom = horible colrs,  horrible form
    # # "dreamlike-photoreal-2.0.ckpt [fc52756a74]",         # makes overly complex images that devolve into chaos
    # #
    #- DELETED

    # "dreamshaper_5BakedVae.safetensors [a60cfaa90d]", 
    # "HassanBlend1.4_Safe.safetensors [b08fdba169]", 
    # "f222.ckpt [9e2c6ceff3]", 
    # "meinamix_meinaV9.safetensors [eac6c08a19]", 
    # "v1-5-pruned-emaonly.safetensors [6ce0161689]", 
    #
    # "modelshoot-1.0.safetensors [80dc271195]", 
    # "openjourney-v4.ckpt [02e37aad9f]", 
    # "chilloutmix_NiPrunedFp32Fix.safetensors [fc2511737a]", 
    # "elldrethsRetroMix_v10.safetensors [57285e7bd5]", 
    #
    # # creates girls :/
    # "ghostmix_v20Bakedvae.safetensors [e3edb8a26f]", 
    # "anythingV3_fp16.ckpt [812cd9f9d9]", 
    # "abyssorangemix3AOM3_aom3a1b.safetensors [5493a0ec49]", 

]
sampler = [
    "Euler a", 
    "Euler", 


    "DPM2 a", 
    "DPM++ 2S a", 
    "DPM++ 2M", 
    "DPM++ SDE", 
#lots of BG noise
    "DPM fast", 
    "DPM adaptive", 
    # "LMS Karras"?,
    "DPM2 Karras", 
    "DPM++ 2S a Karras", 
    "DPM++ 2M Karras", 

    "DPM++ SDE Karras", 
    # "LMS",
    "DPM2", 
    "Heun", 
    "DPM2 a Karras", 
]

#-----------------------------------------------------------------

# uniall = []
# alters1 = []
# alters2 = []
#
# # arrays= [insects, snakes, flowers, fish, birds, animals]
# arrays = [biology]
#
#
# random.shuffle(arrays)
# for a in arrays:
#     nl = random.sample(a,  10)
#     for i in nl:
#         uniall.append(i)
#
# for i in range(len(uniall)):
#     if i%2==0:
#         alters1.append(uniall[i])
#     else:
#         alters2.append(uniall[i])
#
#
# alters1 += alters1
# alters2 += alters2
#
# alters1 = shiftary(alters1)  #^ offset arrays so there are no dups in the pairs
#
