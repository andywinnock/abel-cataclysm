package com.github.L_Ender.cataclysm.client.render.entity.Pet;

import com.github.L_Ender.cataclysm.Cataclysm;
import com.github.L_Ender.cataclysm.client.model.entity.Pet.Bonsly_Model;
import com.github.L_Ender.cataclysm.entity.Pet.Bonsly_Entity;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;

@OnlyIn(Dist.CLIENT)
public class Bonsly_Renderer extends MobRenderer<Bonsly_Entity, Bonsly_Model> {

    private static final ResourceLocation TEXTURE = new ResourceLocation(Cataclysm.MODID, "textures/entity/pet/bonsly.png");

    public Bonsly_Renderer(EntityRendererProvider.Context renderManagerIn) {
        super(renderManagerIn, new Bonsly_Model(), 0.3F);
    }

    @Override
    public ResourceLocation getTextureLocation(Bonsly_Entity entity) {
        return TEXTURE;
    }

    @Override
    protected void scale(Bonsly_Entity entityIn, PoseStack matrixStackIn, float partialTickTime) {
        matrixStackIn.scale(0.8f, 0.8f, 0.8f);
    }
}