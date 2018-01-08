
import numpy as np

class NelderMeadOpt:
    """
    Nelder-Mead optimizer described here
    https://codesachin.wordpress.com/2016/01/16/nelder-mead-optimization/
    """

    def __init__(self, alpha=1, gamma=1.5, beta=0.5):
        self.alpha = alpha
        self.gamma = gamma
        self.beta = beta

    def optimize(self, dim, fn, e = 10**-8, max_iter=5000):
    
        # 1: Baslangic
        # dim fonksiyonun icinde bulundugu uzayin boyutu
        # dim kadar rastgele nokta olustur
        # dim = 3 icin x,y koordinatlarindan olusan ucgen
        # dim = 4 icin x,y,z koordinatlarindan olusan tetrahedron
        points = np.random.rand(dim,dim-1)
        print "Olusturulan noktalar",points
        iter_count = 0
        while iter_count < max_iter:
            iter_count+=1
            # 2: Siralama
            # her biri icin fonksiyonun degerini bul
            results = []
            for p in points:
                p = list(p) # noktalari listeye cevir
                results.append(fn(*p)) # fonksiyona parametre olarak ver
            print "Noktalarin fonksiyon sonuclari",results
            results = np.array(results) # sonuclari NumPy array yap
            indexes = results.argsort() # siralanmis halin indekslerini al
            print "Siralama indisleri",indexes
            results.sort() # sonuclarin kendisini sirala
            print "Siralanmis hali", results
            points = points[indexes] 
            # nokta arrayini siralamak icin sonuclardan elde ettigimiz indisleri kullan
            print "Siralanmis noktalar", points

            # 3: Centroid bul
            centroid = np.mean(points[:-1],axis=0)
            print "Centroid",centroid
            # 4 Transformations: Her iterasyonda en fazla biri gerceklesebilir
            # 4: reflection(Yansima)
            # en kotu noktayi en kotu olmaktan cikar ama en iyi noktadan iyi olmasin
            xr = centroid + self.alpha * (centroid - points[-1]) 
            score_r = fn(*list(xr)) # fonksiyon ciktisini guncelle
            print "R Score", score_r
            if results[0] < score_r <results[-1]:
                points[-1] = xr
                print "Reflection sonrasi noktalar", points
                continue
            # 5: expansion
            if score_r < results[0]:
                xe = centroid + self.gamma * (-points[-1] - centroid)
                score_e = fn(*list(xe))
                print "E Score", score_e
                if score_r > score_e :
                    # eger elde ettigimiz yer en iyi noktadan bile iyiyse biraz daha abart 
                    points[-1] = xe
                    print "Expansion sonrasi noktalar", points
                    continue
                else:
                    points[-1] = xr
                    print "Reflection sonrasi noktalar", points
                    continue
            # 6: contraction
            xc = centroid + self.beta * (points[-1] - centroid)
            score_c = fn(*list(xc))
            print "C Score", score_c
            if score_c < results[-1]:
                # eger gittigimiz yer en kotu ikinci noktadan bile kotuyse geri gelme vakti
                points[-1] = xc
                print "Contraction sonrasi noktalar", points
                continue

            print "Son sonuclar",results

            
        return points[0]

opt = NelderMeadOpt()

fn = lambda x: x**2 + x -5
print opt.optimize(2,fn)
# -0.5

fn = lambda x, y: x**2 + (y-6)**4
print opt.optimize(3,fn)
# 0, 6

fn = lambda x, y, z: x**2 + (y-4)**2 + z**2  # 
print opt.optimize(4,fn)
# 0, 4, 0
